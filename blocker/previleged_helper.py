import os
import tempfile




def update_block_of_hosts(content:str,target_file_path:str = '/etc/hosts'):

    
    target_dir = os.path.dirname(os.path.abspath(target_file_path))
    with tempfile.NamedTemporaryFile(mode='w+',dir=target_dir, delete=False) as tmp_file:
        temp_path = tmp_file.name
        tmp_file.write(content)

    os.chmod(temp_path, 0o644)
    try:
        os.replace(temp_path,target_file_path)
        print("SUCCESSFULLY DONE")
    except OSError:
        print("YOU NEED ADMINISTRATOR PRIVILAGES TO REPLACE IT")
        print("TRY RUNNING IT WITH SUDO")

        os.remove(temp_path)
    