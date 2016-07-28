from StringIO import StringIO
import mock

from cloud.somecomputer import firstmod


class TestFirstMod:

    @mock.patch("cloud.somecomputer.firstmod.write_data", autospec=True)
    @mock.patch("cloud.somecomputer.firstmod.fetch_data", autospec=True)
    @mock.patch("cloud.somecomputer.firstmod.AnsibleModule", autospec=True)
    def test__main__success(self, ansible_mod_cls, fetch_data, write_data):
        # Prepare mocks
        mod_obj = ansible_mod_cls.return_value
        args = {
            "url": "https://www.google.com",
            "dest": "/tmp/somelocation.txt"
        }
        mod_obj.params = args

        # Exercise code
        firstmod.main()

        # Assert call to AsnibleModule
        expected_arguments_spec = dict(
            url=dict(required=True),
            dest=dict(required=False, default="/tmp/firstmod")
        )
        assert(mock.call(argument_spec=expected_arguments_spec) ==
               ansible_mod_cls.call_args)

        # Assert call to fetch_data
        assert(mock.call(mod_obj, args["url"]) == fetch_data.call_args)

        # Assert call to write_data
        assert(mock.call(fetch_data.return_value, args["dest"]) ==
               write_data.call_args)

        # Assert call to mod_obj.exit_json
        expected_args = dict(
            msg="Retrieved the resource successfully",
            changed=True
        )
        assert(mock.call(**expected_args) == mod_obj.exit_json.call_args)

# fetch_data test
    @mock.patch("cloud.somecomputer.firstmod.fetch_url", autospec=True)
    @mock.patch("cloud.somecomputer.firstmod.AnsibleModule", autospec=True)
    def test__fetch_data__success(self, ansible_mod_cls, fetch_url):
        # Mock objects
        mod_obj = ansible_mod_cls.return_value
        url = "https://www.google.com"

        html = "<html><head></head><body></body></html>"
        data = StringIO(html)
        info = {'status': 200}
        fetch_url.return_value = (data, info)

        # Exercise the code
        returned_value = firstmod.fetch_data(mod_obj, url)

        # Assert the results
        expected_args = dict(module=mod_obj, url=url)
        assert(mock.call(**expected_args) == fetch_url.call_args)

        assert(html == returned_value)

# write_data test
    def test__write_data__success(self):
        html = "<html><head></head><body></body></html>"
        dest = "/tmp/somelocation.txt"

        o_open = "cloud.somecomputer.firstmod.open"
        m_open = mock.mock_open()
        with mock.patch(o_open, m_open, create=True):
            firstmod.write_data(html, dest)

        assert(mock.call(dest, "w") == m_open.mock_calls[0])
        assert(mock.call().write(html) == m_open.mock_calls[2])
