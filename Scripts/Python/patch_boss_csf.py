"""Patch Contra generals.csf with the strings required by BAS."""
from pathlib import Path
import struct

REQUIRED = {"INI:FactionBAS": "BOSS", "SIDE:BAS": "BOSS"}


def u32(data, offset):
    return struct.unpack_from("<I", data, offset)[0]


def existing_labels(data):
    names = set()
    pos = 0x18
    end = len(data)
    while pos + 12 <= end:
        if data[pos:pos + 4] != b" LBL":
            break
        pairs = u32(data, pos + 4)
        name_len = u32(data, pos + 8)
        name_start = pos + 12
        name_end = name_start + name_len
        if name_end > end:
            raise ValueError("Malformed CSF: label name exceeds file size")
        names.add(data[name_start:name_end].decode("ascii").upper())
        pos = name_end
        for _ in range(pairs):
            if pos + 8 > end:
                raise ValueError("Malformed CSF: truncated string pair")
            ident = data[pos:pos + 4]
            value_len = u32(data, pos + 4)
            pos += 8 + value_len * 2
            if ident == b"WRTS":
                if pos + 4 > end:
                    raise ValueError("Malformed CSF: truncated extra-value length")
                pos += 4 + u32(data, pos)
            elif ident != b" RTS":
                raise ValueError(f"Malformed CSF: unknown identifier {ident!r}")
            if pos > end:
                raise ValueError("Malformed CSF: string exceeds file size")
    return names


def make_label(name, value):
    n = name.encode("ascii")
    raw = value.encode("utf-16-le")
    encoded = bytes((b ^ 0xFF) for b in raw)
    return b" LBL" + struct.pack("<II", 1, len(n)) + n + b" RTS" + struct.pack("<I", len(value)) + encoded


def patch(path):
    data = path.read_bytes()
    if len(data) < 0x18 or data[:4] != b" FSC":
        raise ValueError(f"Not a Generals/ZH CSF: {path}")
    if u32(data, 4) != 3:
        raise ValueError(f"Unsupported CSF version: {u32(data, 4)}")
    labels = existing_labels(data)
    additions = [make_label(k, v) for k, v in REQUIRED.items() if k.upper() not in labels]
    if not additions:
        return 0
    out = bytearray(data + b"".join(additions))
    struct.pack_into("<I", out, 8, u32(data, 8) + len(additions))
    struct.pack_into("<I", out, 12, u32(data, 12) + len(additions))
    path.write_bytes(out)
    return len(additions)


def OnPreBuild(**kwargs):
    root = Path(__file__).resolve().parents[2]
    csf = root / "generals.csf"
    if not csf.is_file():
        raise FileNotFoundError(f"Required source CSF not found: {csf}")
    print(f"BOSS CSF patch: added {patch(csf)} missing label(s).")


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[2]
    print(f"Added {patch(root / 'generals.csf')} missing label(s).")
