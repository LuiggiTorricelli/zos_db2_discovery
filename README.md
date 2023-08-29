zos_db2_discovery
=================

The Ansible role 'zos_db2_discovery' will perform a sequence of steps to identify Db2 for z/OS subsystems running on either the specific z/OS LPAR or z/OS sysplex where Ansible is connecting to.

Requirements
============

Python and Z Open Automation Utilities must be installed on the remote z/OS system, since the module ibm.ibm_zos_core.zos_operator is used along the role.

Role Variables
==============

Available variables are listed below, along with default values:

    # Identifies if the Db2s should be discovered by SYSPLEX or LPAR
    scope: SYSPLEX
  
Set the scope of the discovery, if it should identify Db2 for z/OS subsystems available only on the connected LPAR or the sysplex. Available options are: [LPAR, SYSPLEX].

Dependencies
============

None.

Example Playbook (with default scope)
=====================================

    - hosts: zos_server
      roles:
        - role: zos_db2_discovery

Example Playbook (with scope being specified)
=============================================

    - hosts: zos_server
      roles:
        - role: zos_db2_discovery
          scope: lpar

Sample Output
=============

When this role is successfully executed, a fact named `zos_db2_discovery_db2_information` will be set. It is a list of dictionaries, with each item being a discovered Db2 for z/OS subsystem and the collected information about it (DDF details, group details, etc.).

    "zos_db2_discovery_db2_information": [
            {
                "ddf": {
                    "aliases": [
                        {
                            "alias": "DBA1SUB1",
                            "port": 15000,
                            "secure_port": 0,
                            "status": "STATIC"
                        },
                        {
                            "alias": "DBA2REST",
                            "port": 0,
                            "secure_port": 8021,
                            "status": "STARTD"
                        },
                    ],
                    "cmtstat": "I",
                    "condbat": 1200,
                    "generic_lu_name": "AMXTUGLU",
                    "ip_address": "::123.456.789.123",
                    "ip_name": "-NONE",
                    "location": "TESTDBA0",
                    "lu_name": "LUTSTDB1",
                    "mdbat": 600,
                    "member_ip_address": "::123.456.789.124",
                    "network_id": "CDN",
                    "resync_domain_name": "DBA1.tst.com",
                    "resync_port": 7001,
                    "secure_port": 0,
                    "sql_domain_name": "testdba0.tst.com",
                    "status": "STARTD",
                    "tcp_port": 7000
                },
                "group": {
                    "catalog_level": "V13R1M100",
                    "current_function_level": "V13R1M100",
                    "group_attach_name": "DBA0",
                    "group_name": "DSNDBA0",
                    "highest_activated_function_level": "V13R1M100",
                    "highest_possible_function_level": "V13R1M500",
                    "lock1_structure_list_entries_in_use": "81",
                    "lock1_structure_number_list_entries": "110481",
                    "lock1_structure_number_lock_entries": "16777216",
                    "lock1_structure_size_kb": "66560",
                    "members": [
                        {
                            "code_level": "131503",
                            "command_prefix": "-DBA1",
                            "identifier": 2,
                            "irlm_procedure": "DBA1IRLM",
                            "irlm_subsystem": "JTU1",
                            "member": "DBA1",
                            "status": "ACTIVE",
                            "subsystem": "DBA1",
                            "system_name": "TSTA"
                        },
                        {
                            "code_level": "131503",
                            "command_prefix": "-DBA2",
                            "identifier": 1,
                            "irlm_procedure": "DBA2IRLM",
                            "irlm_subsystem": "JTU2",
                            "member": "DBA2",
                            "status": "ACTIVE",
                            "subsystem": "DBA2",
                            "system_name": "TSTB"
                        }
                    ],
                    "protocol_level": "2",
                    "sca_structure_in_use": "7%",
                    "sca_structure_size_kb": "14336",
                    "sca_structure_status": "AC",
                    "spt01_inline_length": "32138"
                },
                "owner": "DBA1MSTR",
                "prefix": "-DBA1",
                "subsystem": "DBA1",
                "system": "TSTA"
            }
    ]

License
=======

This role is licensed under licensed under [Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0).

Author Information
==================

This role was created in 2023 by Luiggi Torricelli, a Db2 for z/OS system programmer.
