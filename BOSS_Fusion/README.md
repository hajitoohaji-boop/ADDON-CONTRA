# GLA BOSS Fusion Building

A new building for FactionGLABossGeneral / Side GLABoss.

Rules:
- Maximum 10 contained eligible units.
- Fusion can be requested with an explicit FUSE command at any count from 1 to 10.
- Contained units are inspected dynamically; no pair-by-pair recipe table.
- Inputs are consumed and exactly one deterministic result is produced.
- Vehicles and eligible super-weapon objects are supported where their engine KindOf/containment permits it.

Implementation is staged: the INI shell must not be presented as the finished dynamic fusion system. The actual engine-level inspection/calculation must be implemented and tested before the production BIG is built.
