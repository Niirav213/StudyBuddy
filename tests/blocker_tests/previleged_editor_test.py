from blocker.previleged_helper import update_block_of_hosts
import os

def test_update_block_of_hosts(tmp_path):

    fake_hosts_file = tmp_path / "fake_hosts.txt"
    fake_hosts_file.write_text("127.0.0.1 localhost\n")
    
    # We want to write this new text into the file
    new_content = "127.0.0.1 localhost\n# -- START --\n0.0.0.0 facebook.com\n# -- END --\n"

    # 2. ACTION: Run your function, but point it at the fake file!
    # Because we pass a string, we need to convert the tmp_path object using str()
    result = update_block_of_hosts(new_content, target_file_path=str(fake_hosts_file))

    # 3. ASSERT: Read the fake file to see if the text was actually updated
    content = fake_hosts_file.read_text()
    assert content == new_content
    assert result == 0

    # 4. ASSERT: Check that the permissions were correctly set to 644
    stat = os.stat(fake_hosts_file)
    # oct() converts the file permissions into an octal string. We check the last 3 digits.
    assert oct(stat.st_mode)[-3:] == '644'