from __future__ import absolute_import, division, print_function

__metaclass__ = type
import re

class FilterModule(object):
    def filters(self):
        filters = {
            "parse_group": self.parse_group,
        }
        return filters
    
    def parse_group(self, cmd_response):
        if isinstance(cmd_response, list):
            joined_content = '\n'.join(cmd_response)
        elif isinstance(cmd_response, str):
            joined_content = cmd_response

        # For -DISPLAY GROUP parsing,
        if " DSN7100I " in joined_content:
            msg = "DSN7100I"
            group_name = re.sub(r'[\s\S]+?GROUP\((.*?)[ ]*\)[\s\S]+', r'\1', joined_content).replace('.', '')
            if len(group_name) == 0:
                group_name = None
            catalog_level = re.sub(r'[\s\S]+?CATALOG LEVEL\((.*?)[ ]*\)[\s\S]+', r'\1', joined_content)
            current_function_level = re.sub(r'[\s\S]+?CURRENT FUNCTION LEVEL\((.*?)[ ]*\)[\s\S]+', r'\1', joined_content)
            highest_activated_function_level = re.sub(r'[\s\S]+?HIGHEST ACTIVATED FUNCTION LEVEL\((.*?)[ ]*\)[\s\S]+', r'\1', joined_content)
            highest_possible_function_level = re.sub(r'[\s\S]+?HIGHEST POSSIBLE FUNCTION LEVEL\((.*?)[ ]*\)[\s\S]+', r'\1', joined_content)
            protocol_level = re.sub(r'[\s\S]+?PROTOCOL LEVEL\((.*?)[ ]*\)[\s\S]+', r'\1', joined_content)
            group_attach_name = re.sub(r'[\s\S]+?GROUP ATTACH NAME\((.*?)[ ]*\)[\s\S]+', r'\1', joined_content).replace('.', '')
            if len(group_attach_name) == 0:
                group_attach_name = None
            spt01_inline_length = re.sub(r'[\s\S]+?SPT01 +INLINE +LENGTH: +(\d+)[\s\S]+', r'\1', joined_content)
            # Get member lists
            member_list = re.sub(r'[\s\S]+?( +-+ +-+ +-+ +-+ +-+ +-+ +-+ +-+ +-+[\s\S]+?---------------------)[\s\S]+', r'\1', joined_content)
            found_members = re.findall(r' +(\S+) +(\S+) +(\S+) +(\S+) +(\S+) +(\S+) +(\S+) +(\S+) +(\S+)', member_list)
            found_members.pop(0)
            members = []
            for member in found_members:
                member_name = member[0]
                if member_name.find('....') > -1:
                    member_name = member[2]
                tmp_member = {
                    "member": member_name,
                    "identifier": int(member[1]), 
                    "subsystem": member[2], 
                    "command_prefix": member[3], 
                    "status": member[4], 
                    "code_level": member[5], 
                    "system_name": member[6], 
                    "irlm_subsystem": member[7], 
                    "irlm_procedure": member[8], 
                }
                members.append(tmp_member)
            # Only if data sharing
            sca_structure_size_kb = re.sub(r'[\s\S]+?SCA +STRUCTURE +SIZE: +(\d+)[\s\S]+', r'\1', joined_content)
            sca_structure_status = re.sub(r'[\s\S]+?SCA +STRUCTURE +SIZE: +\d+ +KB, +STATUS= +(\w{2})[\s\S]+', r'\1', joined_content)
            sca_structure_in_use = re.sub(r'[\s\S]+?SCA +IN +USE: +(.+)[\s\S]+', r'\1', joined_content)
            lock1_structure_size_kb = re.sub(r'[\s\S]+?LOCK1 +STRUCTURE +SIZE: +(\d+)[\s\S]+', r'\1', joined_content)
            lock1_structure_number_lock_entries = re.sub(r'[\s\S]+?NUMBER +LOCK +ENTRIES: +(\d+)[\s\S]+', r'\1', joined_content)
            lock1_structure_number_list_entries = re.sub(r'[\s\S]+?NUMBER +LIST +ENTRIES: +(\d+)[\s\S]+', r'\1', joined_content)
            lock1_structure_list_entries_in_use = re.sub(r'[\s\S]+?LIST +ENTRIES +IN +USE: +(\d+)[\s\S]+', r'\1', joined_content)
            if sca_structure_size_kb == joined_content:
                sca_structure_size_kb = None
            if sca_structure_status == joined_content:
                sca_structure_status = None
            if sca_structure_in_use == joined_content:
                sca_structure_in_use = None
            else:
                sca_structure_in_use = sca_structure_in_use.replace(' ', '')
            if lock1_structure_size_kb == joined_content:
                lock1_structure_size_kb = None
            if lock1_structure_number_lock_entries == joined_content:
                lock1_structure_number_lock_entries = None
            if lock1_structure_number_list_entries == joined_content:
                lock1_structure_number_list_entries = None
            if lock1_structure_list_entries_in_use == joined_content:
                lock1_structure_list_entries_in_use = None
            tmp_result = {
                "group_name": group_name,
                "catalog_level": catalog_level,
                "current_function_level": current_function_level,
                "highest_activated_function_level": highest_activated_function_level,
                "highest_possible_function_level": highest_possible_function_level,
                "protocol_level": protocol_level,
                "group_attach_name": group_attach_name,
                "members": members,
                "spt01_inline_length": spt01_inline_length,
                "sca_structure_size_kb": sca_structure_size_kb,
                "sca_structure_status": sca_structure_status,
                "sca_structure_in_use": sca_structure_in_use,
                "lock1_structure_size_kb": lock1_structure_size_kb,
                "lock1_structure_number_lock_entries": lock1_structure_number_lock_entries,
                "lock1_structure_number_list_entries": lock1_structure_number_list_entries,
                "lock1_structure_list_entries_in_use": lock1_structure_list_entries_in_use,
            }
            result = {
                "system": re.findall(r' *(\w+) +.+' + msg + '.+\n', joined_content)[0],
                "datetime": re.findall(r' *\w+ +(.+?) +' + msg + '.+\n', joined_content)[0],
                "content": {
                    "group": tmp_result,
                }
            }
        else:
            result = cmd_response
        return result