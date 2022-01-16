
"""
Runs Joplin CLI commands.
"""

from subprocess import run

VERBOSE = True

def joplin_run(argument, get_output=False):
    """
    Spawns subprocess that runs Joplin argument. 
    Optional kwarg get_output= returns decoded stdout if passed "string" or "list".
    Errors caught and raised in joplin_cli-functions.
    """
    if get_output:
        get_output = get_output.lower()

    if VERBOSE:
        print(f"Calling Joplin: joplin {argument}")

    if not get_output:
        run(f"joplin {argument}", shell=True)
    
    if get_output == "list":
        result = run(f"joplin {argument}", shell=True, capture_output=True)
        result = result.stdout.decode().splitlines()
        if VERBOSE:
            print(result)
        return [i.strip(" ") for i in result]

    if get_output == "string":
        result = run(f"joplin {argument}", shell=True, capture_output=True)
        if VERBOSE:
            print(result)
        return result.stdout.decode()
        
    
