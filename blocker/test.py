from hosts_editor import add_block_to_content

def test_add_block():
    fake_content = ""
    domains = ['facebook.com', 'tiktok.com']
    start_marker = "#---Start---"
    end_marker = "#---End---"
    result = add_block_to_content(fake_content, domains, start_marker, end_marker)


    assert start_marker in result
    assert "0.0.0.0 facebook.com" in result
    assert end_marker in result


def preventing_double_adding_domain():
    start_marker = "#--start--"
    end_marker = "#--end--"

    existing_content = f"{start_marker}\n0.0.0.0 facebook.com\n{end_marker}\n"
    domains = ["facebook.com"]
    result = add_block_to_content(existing_content, domains, start_marker, end_marker)

    start_count = result.count(start_marker)
    assert start_count == 1

