from __future__ import absolute_import, division, print_function

__metaclass__ = type
import re

class FilterModule(object):
    def filters(self):
        filters = {
            "parse_ddf": self.parse_ddf,
        }
        return filters
    
    def parse_ddf(self, cmd_response):
        if isinstance(cmd_response, list):
            joined_content = '\n'.join(cmd_response)
        elif isinstance(cmd_response, str):
            joined_content = cmd_response

        # For -DISPLAY DDF parsing,
        if " DSNL080I " in joined_content:
            msg = "DSNL080I"
            status = re.sub(r'[\S\s]+?DSNL081I +STATUS=(.*)[\S\s]*', r'\1', joined_content)
            location = re.sub(r'[\S\s]+?DSNL083I +(.*?) +[\S\s]*', r'\1', joined_content)
            network_id = re.sub(r'[\S\s]+?DSNL083I +.*? +(.*?)\..* +[\S\s]*', r'\1', joined_content)
            lu_name = re.sub(r'[\S\s]+?DSNL083I +.*? +.*\.(.*?) +[\S\s]*', r'\1', joined_content)
            generic_lu_name = re.sub(r'[\S\s]+?DSNL083I +\S+ +\S+ +(?:.*\.|)(.*|-NONE)[\S\s]*', r'\1', joined_content)
            tcp_port = int(re.sub(r'[\S\s]+?DSNL084I +TCPPORT=(.*?) +[\S\s]*', r'\1', joined_content))
            secure_port = int(re.sub(r'[\S\s]+?DSNL084I +.*SECPORT=(.*?) +[\S\s]*', r'\1', joined_content))
            resync_port = int(re.sub(r'[\S\s]+?DSNL084I +.*RESPORT=(.*?) +[\S\s]*', r'\1', joined_content))
            ip_name = re.sub(r'[\S\s]+?DSNL084I +.*IPNAME=(.*)[\S\s]*', r'\1', joined_content)
            ip_address = re.sub(r'[\S\s]+?DSNL085I +IPADDR=(.*)[\S\s]*', r'\1', joined_content)
            sql_domain_name = re.sub(r'[\S\s]+?DSNL086I +SQL *DOMAIN=(.*)[\S\s]*', r'\1', joined_content)
            aliases = []
            alias_content = re.sub(r'[\s\S]+?( +DSNL087I [\s\S]+?)(?:DSNL090I|DSNL089I)[\s\S]+', r'\1', joined_content)
            if alias_content != joined_content:
                found_aliases = re.findall(r'DSNL088I +(\S+) +(\S+) +(\S+) +(\S+)', joined_content)
                for alias in found_aliases:
                    tmp_alias = {
                        "alias": alias[0],
                        "port": int(alias[1]),
                        "secure_port": int(alias[2]),
                        "status": alias[3],
                    }
                    aliases.append(tmp_alias)
            # Only if data sharing
            resync_domain_name = re.sub(r'[\S\s]+?DSNL086I +RESYNC *DOMAIN=(.*)[\S\s]*', r'\1', joined_content)
            if resync_domain_name == joined_content:
                resync_domain_name = None
            # Only if data sharing
            member_ip_address = re.sub(r'[\S\s]+?DSNL089I +MEMBER IPADDR=(.*)[\S\s]*', r'\1', joined_content)
            if member_ip_address == joined_content:
                member_ip_address = None
            cmtstat = re.sub(r'[\s\S]+?DSNL090I +DT=(\S)[\s\S]+', r'\1', joined_content)
            condbat = int(re.sub(r'[\s\S]+?DSNL090I +DT=\S +CONDBAT= *(\d+)[\s\S]+', r'\1', joined_content))
            mdbat = int(re.sub(r'[\s\S]+?DSNL090I +DT=\S +CONDBAT= *\d+ *MDBAT= *(\d+)[\s\S]+', r'\1', joined_content))
            tmp_result = {
                "status": status,
                "location": location,
                "network_id": network_id,
                "lu_name": lu_name,
                "generic_lu_name": generic_lu_name,
                "tcp_port": tcp_port,
                "secure_port": secure_port,
                "resync_port": resync_port,
                "ip_name": ip_name,
                "ip_address": ip_address,
                "sql_domain_name": sql_domain_name,
                "resync_domain_name": resync_domain_name,
                "aliases": aliases,
                "member_ip_address": member_ip_address,
                "cmtstat": cmtstat,
                "condbat": condbat,
                "mdbat": mdbat,
            }
            result = {
                "system": re.findall(r' *(\w+) +.+' + msg + '.+\n', joined_content)[0],
                "datetime": re.findall(r' *\w+ +(.+?) +' + msg + '.+\n', joined_content)[0],
                "content": {
                    "ddf": tmp_result,
                }
            }
        else:
            result = cmd_response
        return result