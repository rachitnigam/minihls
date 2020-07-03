import argparse
from .lang import Lang


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Process some integers.')

    # Language format for the input.
    parser.add_argument(
        '--input',
        '-i',
        required=True,
        type=Lang.argparse,
        choices=list(Lang)
    )

    # Language format for the output. When unspecified, compile all the way
    # to RTL.
    parser.add_argument(
        '--output',
        '-o',
        default=Lang.RTL,
        type=Lang.argparse,
        choices=list(Lang)
    )

    args = parser.parse_args()

    # Make sure we're trying to compile from a high-level language to a
    # lower-level one.
    assert args.input >= args.output, "Cannot compile from %s to %s." % (
        args.input, args.output)
