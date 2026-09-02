import subprocess 
import pathlib
import time
from blocker.hosts_editor import add_block_to_content, remove_block_from_content

def run_previleged_helper(content: str, target_file_path = '/etc/hosts')-> int:
    combined_input = f"{content}\n{target_file_path}"
    previleged_path = pathlib.Path(__file__).parent.parent / "blocker" / "previleged_helper.py"
    try:

        result = subprocess.run(['pkexec', str(previleged_path), target_file_path], input=content, text=True, capture_output=True)


        print(result.stdout)
        return result.returncode
    except FileNotFoundError:
        print(f"file do not exist on {previleged_path}")
        return -1

    except Exception as e:
        print(f"unexpected error happened: {e}")
        return -1
    
def start_focus_session(duration_minutes: int, domains: list, target_file_path:str):
    try:
        with open(target_file_path, 'r') as f:
            current_content = f.read()
    except FileNotFoundError:
        print("Error: Could not read content")
        return

    blocked_content = add_block_to_content(current_content, domains, '#start\n', '#end\n')
    exit_code = run_previleged_helper(blocked_content, target_file_path)

    if exit_code != 0:
        print("failed to apply block (perhaps authentication was canclled). aborting.")

    try:
        print("focus session applied")
        time.sleep(duration_minutes * 60)
        print("time is up")
    except KeyboardInterrupt:
        print("\nsession interrupted by the user")
    finally:
        print("cleaning up")
        try:
            with open(target_file_path, 'r') as f:
                latest_content = f.read()
            unblocked_content  = remove_block_from_content(latest_content, '#start\n', '#end\n')

            cleanup_code = run_previleged_helper(unblocked_content, target_file_path)

            if cleanup_code == 0:
                print("domain unlocked successfully")
            else:
                print("failed to remove domain.")
        except Exception as e:
            print(f"error during cleanup {e}")

    

if __name__=="__main__":
    target_file_path = '/home/nirav/Projects/StudyBuddy/hosts_test.txt'
    target_file_path1 = '/etc/hosts'
    #result = run_previleged_helper("test content 12\n", '/home/nirav/Projects/StudyBuddy/hosts_test.txt')
    #print("return code: ", result)

    domains = ['m.youtube.com','www.youtube.com']
    start_focus_session(1, domains, target_file_path1)

