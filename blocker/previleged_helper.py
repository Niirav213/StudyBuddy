#!/usr/bin/env python3

import os
import tempfile
import sys




def update_block_of_hosts(content:str,target_file_path:str = '/etc/hosts'):
    temp_path = None
    try:
        target_dir = os.path.dirname(os.path.abspath(target_file_path))
        with tempfile.NamedTemporaryFile(mode='w+',dir=target_dir, delete=False) as tmp_file:
            temp_path = tmp_file.name
            tmp_file.write(content)

        os.chmod(temp_path, 0o644)
    
        os.replace(temp_path,target_file_path)
        print("SUCCESSFULLY DONE")
    except OSError:
        print("YOU NEED ADMINISTRATOR PRIVILAGES TO REPLACE IT")
        print("TRY RUNNING IT WITH SUDO")
        if temp_path:
            os.remove(temp_path)
        return 1
    return 0


if __name__=="__main__":
    content = sys.stdin.read()
    result = update_block_of_hosts(content)
    sys.exit(result)
