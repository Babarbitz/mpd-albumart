pkgname=mpd-albumart
pkgrel=1
pkgver=0.1.0
conflicts=('mpd-albumart')
pkgdesc="Downloads albumart for MPD"
arch=('x86_64')
url="https://github.com/Babarbitz/mpd-albumart"
license=('GPL3')
depends=('python' 'mpd' 'python-mpd2' 'python-requests' 'python-fuzzywuzzy')
makedepends=('python-build'
             'python-installer'
             'python-wheel')
source=("https://github.com/Babarbitz/mpd-albumart/archive/v${pkgver}.tar.gz")
sha256sums=('SKIP')
build() {
    cd "$srcdir/$pkgname-$pkgver"
    python -m build --wheel --no-isolation
}

package() {
    cd "$srcdir/$pkgname-$pkgver"
    python -m installer --destdir="$pkgdir" dist/*.whl
}
