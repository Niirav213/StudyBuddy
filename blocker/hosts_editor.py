

def add_block_to_content(content: str, domains: list[str], start_marker: str, end_marker: str)-> str:
    # it appends formated block of domains to the existing hosts content.
    if not domains:
        return content
    block_lines = [start_marker]
    for domain in domains:
        block_lines.append(f"0.0.0.0 {domain}")
    block_lines.append(end_marker)

    content = remove_block_from_content(content, start_marker,end_marker)

    block_text = "\n".join(block_lines) + "\n"

    if content and not content.endswith('\n'):
        content += "\n"
    return content + block_text

def remove_block_from_content(content: str, start_marker: str, end_marker: str)-> str:
    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)

    if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
        end_slice_idx = end_idx + len(end_marker)

        if end_slice_idx < len(content) and content[end_slice_idx] == '\n':
            end_slice_idx += 1

        return content[:start_idx] + content[end_slice_idx:]
    return content
