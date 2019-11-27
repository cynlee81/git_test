import ldclient
import logging
import time
from ldclient.config import Config
from ldclient.integrations import Redis
from ldclient.feature_store import CacheConfig
from ldclient.file_data_source import FileDataSource


client = None


def test_json():
    flag = "test_json"

    vid = "vid15"
    user = {
        "key": "vendor_" + vid,
        "custom": {
            "vid": vid,
            "region": "US",
        },
    }

    enabled = client.variation(flag, user, "Unknown")

    print("\nXXXX %s is enabled: %s\n" % (flag, enabled))


def test_1(vid):
    flag = "test1"
    user = {
        "key": "vendor_" + vid,
        "custom": {
            "vid": vid,
            "region": "US",
        },
    }

    enabled = client.variation(flag, user, "Unknown")

    print("\nXXXX %s is enabled: %s\n" % (flag, enabled))


def test_1_1():
    flag = "test1-1"

    vid = "vid12"
    user = {
        "key": "vendor_" + vid,
        "custom": {
            "vid": vid,
            "region": "US",
        },
    }

    enabled = client.variation(flag, user, "Unknown")

    print("\nXXXX %s is enabled: %s\n" % (flag, enabled))


def register_user(vid):
    user = {
        "key": "vendor_" + vid,
        "custom": {
            "vid": vid,
            "region": "US",
            "name": "Company " + vid
        },
    }

    client.identify(user)

if __name__ == "__main__":
    def setup_logger():
        ldclient.log.setLevel(logging.DEBUG)
        ldclient.log.addHandler(logging.StreamHandler())

    def use_datastore(config):
        # default url is localhost:6379
        store = Redis.new_feature_store(
            # url='redis://my-redis:6379',
            prefix='test', caching=CacheConfig(expiration=30))

        config.feature_store = store
        config.use_ldd = False

    def use_file(config):
        factory = FileDataSource.factory(paths=["file1.json", "file2.json"],
                                         auto_update=True)

        config.update_processor_class = factory
        config.send_events = False

    print("******** SETUP ********")
    setup_logger()
    use_relay_proxy = False
    if use_relay_proxy:
        proxy = "http://10.42.254.186:8030"
        config = Config(base_uri=proxy, stream_uri=proxy, events_uri=proxy)
    else:
        config = Config()
    #use_datastore(config)
    #use_file(config)

    ldclient.set_config(config)
    ldclient.set_sdk_key("sdk-ce3ef6b6-a464-4eba-af38-cde63f660e55")

    print("******** INIT ********")
    client = ldclient.get()

    print("******** TEST ********")
    enabled = ldclient.get().variation("test1", {}, "Unknown")
    test_1("vid11")
    #test_1("vid12")
    #test_1("vid13")

    #register_user("vid14")

    time.sleep(30)

    print("******** CLOSE ********")
    client.close()

    # cache size
    # logging level
