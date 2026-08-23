import subprocess 
import pathlib
import sys

def run_previleged_helper(content: str, target_file_path = '/etc/hosts')-> int:
    combined_input = f"{content}\n{target_file_path}"
    previleged_path = pathlib.Path(__file__).parent.parent / "blocker" / "previleged_helper.py"
    try:

        result = subprocess.run(['pkexec', previleged_path], input=combined_input, text=True, capture_output=True)


        print(result.stdout)
        return result.returncode
    except FileNotFoundError:
        print(f"file do not exist on {previleged_path}")
        return -1

    except Exception as e:
        print(f"unexpected error happened: {e}")
        return -1
    

if __name__=="__main__":
    content = sys.stdin.read()
    result = run_previleged_helper("test content 112\n", '/home/nirav/Projects/StudyBuddy/hosts_test.txt')
    print("return code: ", result)