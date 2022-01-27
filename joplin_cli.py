
"""
    Joplin Command Line Interface (CLI) API for Python
    https://joplinapp.org/

    WARNING: Running Joplin CLI while using this API is likely bad.
"""

from helpers import *


def attach(note, file_path):
    """ 
        Attaches the given file to the note.

        See the alternative attach_() from joplin_cli_extended.py
    """
    
    result = joplin_run(f"attach {give_quotes(note)} {give_quotes(file_path)}", get_output="string")
    
    if "Cannot find" in result:
        raise ValueError("Cannot find note.")
    if "Cannot access" in result:
        raise ValueError("Cannot access file. Did you forget to enclose path in quotes - 'path'?")


def batch(path_to_file):
    """Runs the commands contained in the text file. There should be one command per line."""
    
    joplin_run(f"batch {path_to_file}")


def cat(note, verbose=False):
    """Displays the given note. Add "verbose=True" to get the complete information about the note."""
    
    if verbose:
        return joplin_run(f"cat {give_quotes(note)} -v", get_output="string")
    else:
        return joplin_run(f"cat {give_quotes(note)}", get_output="string")


def config(name=None, value=None, verbose=False, export=False):
    """
    Gets or sets a config value.

    If neither name or value is provided, it returns the current configuration as a string.
    To get a specific config value, pass name only.
    To set a specific config value, pass name and value.
    
    Does not currently support import or import from file.
    For more, use Joplin "help config"
    """
    argument = "config "

    if name not in ["sync.target", "sync.2.path","sync.5.path","sync.5.username","sync.5.password","sync.6.path","sync.6.username","sync.6.password","sync.8.path","sync.8.url","sync.8.region","sync.8.username","sync.8.password","sync.8.forcePathStyle","sync.9.path","sync.9.username","sync.9.password","sync.10.username","sync.10.password","sync.maxConcurrentConnections","locale","dateFormat","timeFormat","uncompletedTodosOnTop","showCompletedTodos","notes.sortOrder.field","notes.sortOrder.reverse","folders.sortOrder.field","folders.sortOrder.reverse","trackLocation","sync.interval","editor","net.customCertificates","net.ignoreTlsErrors","sync.wipeOutFailSafe","revisionService.enabled","revisionService.ttlDays","layout.folderList.factor","layout.noteList.factor","layout.note.factor",]:
        raise ValueError("Incorrect config name")
    argument += str(" " + name + " ")

    if value:
        argument += give_quotes(value)
    if verbose:
        argument += " -v"
    if export:
        argument += " -export"

    result = joplin_run(argument, get_output="string")
    if "Unknown key" in result:
        raise ValueError("Unknown value.")
    if "Error opening note in editor: spawnSync C:Windowsnotepad.exe ENOENT" in result:
        raise EnvironmentError("Error opening note in editor: spawnSync C:Windowsnotepad.exe ENOENT")


def cp(note, notebook):
    """ Duplicates the notes matching "note" to "notebook". If no notebook is specified the note is duplicated in the current notebook. """
    if not note or type(note) != str:
        raise ValueError("Invalid note name.")
    if not notebook or type(notebook) != str:
        raise ValueError("Invalid note name.")
    
    result = joplin_run(f"cp {give_quotes(note)} {give_quotes(notebook)}", get_output="string")
    
    if "Cannot find" in result:
        raise ValueError("Invalid note and/or notebook name")
    else:
        return result


def done(name_of_todo):
    """Marks a to-do as done."""
    result = joplin_run(f"done {give_quotes(name_of_todo)}", get_output="string")
    if "Cannot find" in result:
        raise ValueError("No todo by that name")
    if "Note is not a to-do:" in result:
        raise ValueError("Note is not a to-do.")


def e2ee(command_, path, **kwargs):
    """ 
    e2ee <command> [path]

    Manages E2EE configuration. Commands are "enable", "disable", "decrypt", "status", "decrypt-file", and "target-status".
    
    Options (use kwargs option1="-p password", option2="-v" etc.)
        -p, --password <password>   Use this password as master password (For security reasons, it is not recommended to use this option).
        -v, --verbose               More verbose output for the `target-status` command
        -o, --output <directory>    Output directory
        --retry-failed-items        Applies to `decrypt` command - retries decrypting items that
                                    previously could not be decrypted.
     """
 
    if command_ not in ["enable", "disable", "decrypt", "status", "decrypt-file", "target-status"]:
        raise ValueError("Invalid command")
    
    if path is None and command_ not in ["enable", "disable", "status"]:
        raise ValueError("Missing path argument.")
    
    argument = f"e2ee {command_} {give_quotes(path)}"

    for kwarg in kwargs:
        argument += give_quotes(kwarg)
    
    return joplin_run(argument, get_output="string")


def edit(note):
    """Not implemented. Feel free to help out!"""
    

def export(note=None, notebook=None, format_=None, path=None):
    """
    Exports Joplin data to the given path. By default, it will export the complete database including notebooks, notes, tags and resources. 
    
    Formats:
        - "jex"             Joplin Export File
        - "raw"             Joplin Export Directory
        - "md"              Markdown
        - "md_frontmatter"  Markdown + Front Matter
    
    E.g. export(notebook="My Notebook", format="md", path="C:\\JoplinExport")
    """
    if format_ not in ["jex", "raw", "md", "md_frontmatter"]:
        raise ValueError("Invalid format.")
    if format_ is None or path is None:
        raise ValueError("Both format and path must be specified.")
    if note is not None and notebook is not None:
        raise ValueError("You can only specify a note or a notebook. Not both.")
    
    if note:
        argument = f"export --note {give_quotes(note)} --format {format_} {give_quotes(path)}"
    if notebook:
        argument = f"export --notebook {give_quotes(notebook)} --format {format_} {give_quotes(path)}"
    if not note and not notebook:
        argument = f"export --format {format_} {give_quotes(path)}"

    result = joplin_run(argument, get_output="string")
    
    if "Cannot find" in result:
        raise ValueError("Cannot find note/notebook.")
    if "contains invalid WIN32 path characters" in result:
        raise ValueError("Path contains invalid WIN32 path characters. Use escapes, and do not end with \\.")


def geoloc(note):
    """ Displays a geolocation URL for the note or notebook."""
    result = joplin_run(f"geoloc {give_quotes(note)}", get_output="string")
    if "Cannot find" in result:
        raise ValueError("No such note.")
    else:
        return result
    

def help(topic):
    """Returns string of usage information. Might be easier to do this manually in a terminal window."""
    if str(topic) in ["attach", "batch", "cat", "config", "cp", "done", "e2ee", "edit", "export", "geoloc", "help", "import", "ls", "mkbook", "mknote", "mktodo", "mv", "ren", "rmbook", "rmnote", "server", "set", "status", "sync", "tag", "todo", "undone", "use", "version"]:
        return joplin_run(f"help {topic}", get_output="string")
    

def import_(data, notebook, format_="auto", output_format=None, force=True):
    """
    Imports data into Joplin.

    format                Source format: auto, jex, md, md_frontmatter, raw, enex
    force                 Do not ask for confirmation (True by default to avoid prompts.)
    output-format         Output format: md, html
    """
    
    if format_ not in ["auto", "jex", "md", "md_frontmatter", "raw", "enex"]:
        raise ValueError("Invalid format.")
    if not data or not notebook:
        raise ValueError("Must provide data and target notebook.")
    
    argument = f"import --format {format_} {give_quotes(data)} {give_quotes(notebook)}"

    if output_format:
        argument += give_quotes(output_format)
    
    if force:
        argument += " -f"

    result = joplin_run(argument, get_output="string")
    if "Cannot find" in result:
        raise ValueError("Cannot find data or notebook.")


def ls(*args):
    """Empty call returns list of notes in current notebook. Add each as kwarg, e.g. ls(option1="-/", option2= ... )

        /                      Displays the list of notebooks
        -n, --limit <num>      Displays only the first top <num> notes.
        -s, --sort <field>     Sorts the item by <field> (eg. title, updated_time, created_time).
        -r, --reverse          Reverses the sorting order.
        -t, --type <type>      Displays only the items of the specific type(s). Can be `n` for notes, `t` for to-dos, or `nt` for notes and to-dos (eg. `-tt` would display only the to-dos, while `-tnt` would display notes and to-dos.
        -f, --format <format>  Either "text" or "json"
        -l, --long             Use long list format. Format is ID, NOTE_COUNT (for notebook), DATE, TODO_CHECKED (for to-dos), TITLE
    """
    argument = ""
    for arg in args:
        if arg not in ["/", "-n", "-s", "-r", "-t", "-f", "-l"]:
            raise ValueError("One or more of your arguments are not among the listed options. Please revise your call.")
        else:
            argument += arg

    return joplin_run(f"ls {argument}", get_output="list")


def mkbook(name):
    """Creates a new notebook"""
    joplin_run(f"mkbook {give_quotes(name)}")


def mknote(name):
    """Creates new note in most recently selected notebook"""
    joplin_run(f"mknote {give_quotes(name)}")


def mktodo(name):
    """Creates a new to-do in most recently selected notebook"""
    joplin_run(f"mktodo {give_quotes(name)}")


def mv(note, notebook):
    """Looks for note in currently selected notebook, and, if found, moves it to the specified notebook.
    It seems Joplin also changes the corrent notebook during this process, so call use() prior to each call to mv().
    
    You may find the mv_() function from joplin_cli_extended.py useful.
    """
    result = joplin_run(f"mv {give_quotes(note)} {give_quotes(notebook)}", get_output="string")
    if "Cannot find" in result:
        raise ValueError("No note or notebook by that name")


def ren(old, new):
    """Renames the given note, todo, or notebook"""
    result = joplin_run(f"ren {give_quotes(old)} {give_quotes(new)}", get_output="string")
    if "Cannot find" in result:
        raise ValueError("No note, todo, or notebook by that name")


def rmbook(notebook):
    """Deletes the given notebook without asking for confirmation"""
    result = joplin_run(f"rmbook {give_quotes(notebook)} -f", get_output="string")
    if "Cannot find" in result:
        raise ValueError("No notebook by that name")


def rmnote(note):
    """Deletes the given note without asking for confirmation"""
    result = joplin_run(f"rmnote {give_quotes(note)} -f", get_output="string")
    if "Cannot find" in result:
        raise ValueError("No note by that name")


def server(server_command):
    """
    WARNING -- UNTESTED FUNCTION -- Will pass any string as final argument of "joplin server"-command.

    Start, stop or check the API server. To specify on which port it should run, set the api.port
    config variable. Commands are (start|stop|status). This is an experimental feature - use at your
    own risks! It is recommended that the server runs off its own separate profile so that no two
    CLI instances access that profile at the same time. Use --profile to specify the profile path."""
    if server_command is str:
        joplin_run(f"server {give_quotes(server_command)}")


def set_(note, property_, value):
    """ Sets the property of the given note to the given value. 
    Possible properties are:
        parent_id (text), 
        title (text), 
        body (text), 
        created_time (int), 
        updated_time (int), 
        is_conflict (int), 
        latitude (numeric), 
        longitude (numeric), 
        altitude (numeric), 
        author (text), 
        source_url (text), 
        is_todo (int), 
        todo_due (int), 
        todo_completed (int), 
        source (text), 
        source_application (text), 
        application_data (text), 
        order (numeric), 
        user_created_time (int), 
        user_updated_time (int), 
        encryption_cipher_text (text), 
        encryption_applied (int), 
        markup_language (int), 
        is_shared (int), 
        share_id (text), 
        conflict_original_id (text), 
        master_key_id (text).
    """

    set_properties = ["parent_id", "title", "body", "created_time", "updated_time", "is_conflict", "latitude", 
                    "longitude", "altitude", "author", "source_url", "is_todo", "todo_due", "todo_completed", 
                    "source", "source_application", "application_data", "order", "user_created_time", "user_updated_time", 
                    "encryption_cipher_text", "encryption_applied", "markup_language", "is_shared", "share_id", 
                    "conflict_original_id", "master_key_id"]

    if property_ not in set_properties:
        raise ValueError("No such property.")
    
    joplin_run(f"set {give_quotes(note)} {property_} {value}")


def status(get_string=False):
    """Returns output from Joplin "status" list of strings, one per line, by default. Optional kwarg returns string."""
    if get_string:
        return joplin_run("status", get_output="string")
    
    return joplin_run("status", get_output="list")


def sync():
    """Synchronises with remote storage"""
    joplin_run("sync")


def tag(tag_command, tag=None, note=None, long=False):
    """
        Descriptions ...            Arguments
        Add tag to note:            ("add", "tag", "note")
        Remove tag from note:       ("remove", "tag", "note")
        List tags on note:          ("notetags", "note")
        List tags in use:           ("list")
        List tags in use (long):    ("list", long=True)
        
        "long" format: ID, NOTE_COUNT (for notebook), DATE, TODO_CHECKED (for to-dos), TITLE
    """

    if type(tag_command) is not str or tag_command not in ["add", "remove", "list", "notetags", "tag list"]:
        raise ValueError("Invalid argument passed as \"tag_command\"")

    if tag_command == "list" and long is True:
        return joplin_run(f"tag list -l", get_output="string")

    if tag_command == "list":
        result = joplin_run(f"tag list {give_quotes(note)}", get_output="string")   
        if "Cannot find" in result:
            raise ValueError("Invalid note name.")    
        return result
    
    if tag_command == "notetags":
        if note is None:
            raise ValueError("Must specify note to call notetags")
        return joplin_run(f"tag notetags {give_quotes(note)}", get_output="string")
    
    if tag == None or note == None:
        raise ValueError("Must specify both tag and note to add or remove tags.")
    
    else:
        joplin_run(f"tag {tag_command} {give_quotes(tag)} {give_quotes(note)}")
    
    
def todo(command, name):
    """
    The command "toggle" toggles status of named to-do, or coverts note to to-do. 
    The command "clear" converts to-do back to regular note.
    """
    if command == "toggle":
        result = joplin_run(f"todo toggle {give_quotes(name)}", get_output="string")        
        if "Cannot find" in result:
            raise ValueError("No todo by that name")
        if "Note is not a to-do:" in result:
            raise ValueError("Note is not a to-do.")

    if command == "clear":
        joplin_run(f"todo clear {give_quotes(name)}", get_output="string")
    
    if command != "toggle" and command != "clear":
        raise ValueError("Invalid command.")


def undone(todo):
    """Marks a to-do as non-completed."""
    result = joplin_run(f"undone {give_quotes(todo)}", get_output="string")
    if "Cannot find" in result:
        raise ValueError("No todo by that name")
    if "Note is not a to-do:" in result:
        raise ValueError("Note is not a to-do.")


def use(notebook):
    """Switches to notebook, if it exists."""
    result = joplin_run(f"use {give_quotes(notebook)}", get_output="string")
    if "Cannot find" in result:
        raise ValueError("No notebook by that name")


def version():
    """Returns string containing version information."""
    return joplin_run("version", get_output="string")
