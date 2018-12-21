import modelplane.about as about

from modelplane.gfx.viewer import Viewer

_WIDTH = 1000
_HEIGHT = 800


def main():
    print(f'{about.MP_TITLE} version {about.MP_VERSION}')
    viewer = Viewer(_WIDTH, _HEIGHT, about.MP_TITLE)
    viewer.main_loop()


if __name__ == '__main__':
    main()
