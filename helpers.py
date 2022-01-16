
"""
Helper functions
"""

def give_quotes(a_string):
    """Ensures string begins and ends with double-quotes. Removes them anywhere else."""
    quotes = a_string.count("'") + a_string.count('"')
    if quotes > 2:
        raise ValueError("Unable to process name of notebook, note, todo or file. No quotes allowed in string or filename.")


    if "'" in a_string:
        a_string = a_string.replace("'", "")
    if '"' in a_string:
        a_string = a_string.replace('"', "")

    return f"\"{a_string}\""
    
