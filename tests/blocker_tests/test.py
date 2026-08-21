from blocker.hosts_editor import add_block_to_content, remove_block_from_content

def test_add_block():
    fake_content = ""
    domains = ['facebook.com', 'tiktok.com']
    start_marker = "#---Start---"
    end_marker = "#---End---"
    result = add_block_to_content(fake_content, domains, start_marker, end_marker)


    assert start_marker in result
    assert "0.0.0.0 facebook.com" in result
    assert end_marker in result


def test_preventing_double_adding_domain():
    start_marker = "#--start--"
    end_marker = "#--end--"

    existing_content = f"{start_marker}\n0.0.0.0 facebook.com\n{end_marker}\n"
    domains = ["facebook.com"]
    result = add_block_to_content(existing_content, domains, start_marker, end_marker)

    start_count = result.count(start_marker)
    assert start_count == 1

def test_partial_or_broken_markers():
    start_marker = "#--start--"
    end_marker = "#--end--"

    content_missing_end = f"127.0.0.1 localhost\n{start_marker}\n0.0.0.0 facebook.com\n"

    result_a = remove_block_from_content(content_missing_end, start_marker, end_marker)

    assert result_a == content_missing_end

    content_reverse_marked = f"{end_marker}\n0.0.0.0 facebook.com\n{start_marker}\n"

    result_b = remove_block_from_content(content_reverse_marked, start_marker, end_marker)

    assert result_b == content_reverse_marked