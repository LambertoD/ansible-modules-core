#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import fetch_url

# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

DOCUMENTATION = '''
---
module: firsmod
short_description: Downloads stuff from the interwebs
description:
    - Downloads stuff
    - Saves said stuff
version_added: "2.2"
options:
  url:
    description:
      - The location of the stuff to download
    required: false
    default: null
  dest:
    description:
      - Where to save the stuff
    required: false
    default: /tmp/firstmod

author:
    - "Your Name Here (@yourgithubusernamehere)"
'''

RETURN = '''
msg:
    description: Just returns a friendly message
    returned: always
    type: string
    sample: Hi there!
'''

EXAMPLES = '''
# Just download it
- firstmod:
    url: https://www.google.com

# Download then save to your home dir
- firstmod:
    url: https://www.relaxdiego.com
    dest: ~/relaxdiego.com.txt
'''


def main():
    mod = AnsibleModule(
        argument_spec=dict(
            url=dict(required=True),
            dest=dict(required=False, default="/tmp/firstmod")
        )
    )

    data = fetch_data(mod, mod.params["url"])
    write_data(data, mod.params["dest"])

    mod.exit_json(msg="Retrieved the resource successfully", changed=True)


def fetch_data(mod, url):
    data, info = fetch_url(module=mod, url=url)
    return data.read()


def write_data(data, dest):
    with open(dest, 'w') as dest:
        dest.write(data)

if __name__ == '__main__':
    main()
