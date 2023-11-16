pkgname=mpd-albumart
pkgrel=1
pkgver=0.0.1
conflicts=('mpd-albumart')
pkgdesc="Downloads albumart for MPD"
arch=('x86_64')
url="https://github.com/Babarbitz/mpd-albumart"
license=('GPL3')
depends=('python' 'mpd' 'python-mpd2' 'python-requests')
makedepends=('python-build'
             'python-installer'
             'python-wheel')
source=("git+https://github.com/Babarbitz/mpd-albumart#tag=v$pkgver")
sha256sums=('SKIP')
pkgver() {
    cd "$pkgname"
    git describe --long --tags | sed 's/\([^-]*-g\)/r\1/;s/-/./g;s/^v//'
}

build() {
    cd mpd-albumart
    python -m build --wheel --no-isolation
}

package() {
    cd "$srcdir/$pkgname"
    python -m installer --destdir="$pkgdir" dist/*.whl
}
