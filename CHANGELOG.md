# CHANGELOG



## v0.1.0 (2024-01-07)

### Chore

* chore: Updated build configuration

Added build command to `pyprojectl.toml` and added `PKGBUILD` ([`3e5bd51`](https://github.com/Babarbitz/mpd-albumart/commit/3e5bd51a338a223c32a36fe292be4fc292eb0550))

### Feature

* feat: Added fuzzy string matching for lookups ([`152640b`](https://github.com/Babarbitz/mpd-albumart/commit/152640bf94469e1f5916ebfa96aa1b39151c71df))

### Unknown

* Updated package build ([`22e0570`](https://github.com/Babarbitz/mpd-albumart/commit/22e0570bb1b42b2d7743674d1e5fc8f1d539ce56))


## v0.0.1 (2023-11-16)

### Fix

* fix: added check for album artist folder

- Fixes path error when saving art ([`f3668d5`](https://github.com/Babarbitz/mpd-albumart/commit/f3668d5ba22c3a185ba2c6eac81e018e810dc876))

* fix: Added explicit checks for album/albumartist keys

- Fixes exception in `mpd_update_album_art` when albumartist or album is not
  defined in the metadata for a song from mpd ([`2f14b92`](https://github.com/Babarbitz/mpd-albumart/commit/2f14b920f1bc076e267b5a38f50964817caadb77))


## v0.0.0 (2023-11-13)

### Unknown

* Initial commit ([`4f612a0`](https://github.com/Babarbitz/mpd-albumart/commit/4f612a0673b93982f4e61e2a40f063ea84209297))
