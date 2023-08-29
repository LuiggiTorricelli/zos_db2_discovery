from __future__ import absolute_import, division, print_function

__metaclass__ = type
import re

class FilterModule(object):
    def filters(self):
        filters = {
            "parse_opdata": self.parse_opdata,
        }
        return filters
    
    def parse_opdata(self, cmd_response):
        if isinstance(cmd_response, list):
            joined_content = '\n'.join(cmd_response)
        elif isinstance(cmd_response, str):
            joined_content = cmd_response

        # For D OPDATA parsing,
        if " IEE603I " in joined_content:
            msg = "IEE603I"
            entries = re.findall(r'^ +(\S+) +(\S+) +(\S+) +(\S+) +(\S+) +(\S+)', joined_content, re.MULTILINE)
            entries.pop(0)
            command_prefixes = []
            for entry in entries:
                tmp_result = {
                    "prefix": entry[0],
                    "owner": entry[1],
                    "system": entry[2],
                    "scope": entry[3],
                    "remove": entry[4],
                    "faildsp": entry[5],
                }
                command_prefixes.append(tmp_result)
            result = {
                "system": re.findall(r' *(\w+) +.+' + msg + '.+\n', joined_content)[0],
                "datetime": re.findall(r' *\w+ +(.+?) +' + msg + '.+\n', joined_content)[0],
                "content": {
                    "command_prefixes": command_prefixes,
                }
            }
        else:
            result = cmd_response
        return result