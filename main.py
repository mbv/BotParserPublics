from config import Config
from getter import Getter
from sender import Sender


def main():
    config = Config()
    getter = Getter(config)
    sender = Sender(config)
    sender.send_posts(getter.get())


if __name__ == '__main__':
    main()