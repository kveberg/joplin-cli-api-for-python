"""
Tests for joplin_cli.py & joplin_cli_extended.py
"""
import logging

from joplin_cli import *
from joplin_cli_extended import *
from helpers import *
from os import getcwd

test_int = 1
test_string = "Test"
test_float = 0.284
test_object = logging.getLogger()
test_ugly_list = [test_int, test_string, test_float, test_object]
test_dict = {test_int:test_string, test_object:test_float}
test_path = "C:\\JoplinTesting"

test_book = "test book"
test_todo = "test todo"
test_note = "test note"
test_tag = "test tag"
test_tag2 = "test tag2"
test_notetag = "test notetag"

cwd = getcwd()
test_file_path = (f"\"{cwd}\\test_file.txt\"")


"""batch"""
# batch(test_file_path)


"""cat"""
# mkbook("test book")
# import_(test_file_path, "test book")
# use("test book")
# print(cat("test_file"))
# print(cat("test_file", verbose=True))
# rmbook("test book")


"""config""" 
# print(config(name="locale"))
# print(config(name="locale", value="not_a_language"))


"""cp"""
# mkbook("test book")
# mkbook("test_book2")
# mknote("note1")
# cp("note1", "test book")


"""e2ee"""
# print(e2ee("status", test_path, option1="-v"))


"""export"""
# export(notebook=test_book, format_="md", path="C:\\JoplinExport")


"""geoloc"""
# mkbook(test_book)
# mknote(test_note)
# print(geoloc(test_note))


"""help"""
# print(help("cp"))


"""import"""
# mkbook(test_book)
# import_(test_file_path, test_book)

"""ls - NO """
# print(ls())
# print(ls("/"))
# print(ls("-f"))

"""server"""
# NOT TESTED.

"""set_"""
# mkbook(test_book)
# mknote(test_note)
# set_(test_note, "author", "Foo")
# set_(test_note, "bakert", "foo")
# rmbook(test_book)


"""status"""
# print(status())
# print(status(get_string=True))


"""sync"""
# sync()


"""tag"""
# mkbook(test_book)
# use(test_book)
# mknote(test_note)
# tag("add", test_tag, test_note)

# a_tag = tag("list", note=test_note)
# print(f"This is a tag saying ... {test_tag}: {a_tag}")

# tag("add", test_tag2, test_note)
# print(tag("list", long=True))

# print(f"There should be tags: {tag('notetags', note=test_note)}")
# tag("remove", test_tag, test_note)
# tag("remove", test_tag2, test_note)
# print(f"There should not be tags: {tag('notetags', note=test_note)}")
# rmbook("test book")


"""version"""
# print(version())


"""
NOTEBOOKS, NOTES & TODOs
Notebooks  use, create, rename, delete
Notes           create, rename, delete, move, toggle, attach
Todos           create, rename, delete, move, toggle, attach, clear, done, undone

ASSUMPTIONS:
   1) give_quotes() works
   2) no duplicate names (Joplin works this way)
"""
# mkbook("test book 1")
# mkbook("test book 2")

# use("test book 1")
# mknote("test note 1")
# mktodo("test todo 1")
# done("test todo 1")
# mv("test todo 1", "test book 2")
# use("test book 1")
# mv("test note 1", "test book 2")

# use("test book 2")
# mknote("test note 2")
# mktodo("test todo 2")
# done("test todo 2")
# mv("test todo 2", "test book 1")
# use("test book 2")
# mv("test note 2", "test book 1")

# undone("test todo 1")
# use("test book 1")
# undone("test todo 2")

# use("test book 1")
# todo("toggle", "test note 2")
# todo("toggle", "test todo 2")
# use("test book 2")
# todo("clear", "test todo 1")

# ren("test note 1", "testn 1")
# ren("test todo 1", "testt 1")
# ren("test book 2", "testb 2")

# use("testb 2")
# rmnote("testt 1")
# rmnote("testn 1")
# rmbook("testb 2")

# use("test book 1")
# attach("test note 2", test_file_path)
# attach("test todo 2", test_file_path)

# rmnote("test todo 2")
# rmnote("test note 2") 
# rmbook("test book 1")
