import os
import sys
import shutil
import uuid
import re

# Configuration:
emptydirs_file_name = ".emptydirs"
# This is neccessary because you cant push empty dirs in git.
# But if you use it on your local computer you can just create empty directories in your template folder!
# But dont delete this file as it is used to identify template directories in input mode (not when specified by commandline)!

args = sys.argv[1:]
working_dir = os.path.dirname(os.path.realpath(__file__))

try:
    input = raw_input # python 2.x compatibility
except NameError:
    pass

def legit_dir(r):
	f = os.path.join(working_dir, r)

	return not os.path.isfile(f) and os.path.exists(os.path.join(f, emptydirs_file_name))

auto_template_dirs = [f for f in os.listdir(working_dir) if legit_dir(f)]

if "-i" in args:
	for i, x in enumerate(auto_template_dirs):
		print(str(i + 1) + ": " + x)

	a = input("Slect template (number or name): ")
	try:
		num = int(a) - 1
		if num >= len(auto_template_dirs) or num < 0:
			print("Please input a valid number")
			sys.exit(0)

		a = auto_template_dirs[num]
	except ValueError:
		if a not in auto_template_dirs:
			print("Please input a valid number or name")
			sys.exit(0)
	template_dir_name = a
	
	project_name = input("Enter project name: ").strip()
	if not project_name:
		print("Please input a valid name")
		sys.exit(0)
		
elif len(args) != 2:
	print("Usage: " + os.path.basename(__file__) + " [-i] [TEMPLATE NAME] [PROJECT NAME]")
	print("\t-i\task me for input")
	sys.exit(0)
else:
	template_dir_name = args[0].strip()
	project_name = args[1].strip()

uuid_re = re.compile(r"\{\$UUID_([0-9]+)\$\}")

if project_name == template_dir_name:
	print("Project name cannot be the same as template directory name")
	sys.exit(0)

if project_name in auto_template_dirs:
	print("The creation would replace a template... aborting")
	sys.exit(0)	

project_dir = os.path.join(os.getcwd(), project_name)
template_dir = os.path.join(working_dir, template_dir_name)
emptydirs_file = os.path.join(template_dir, emptydirs_file_name)

if not os.path.exists(template_dir):
	print("Template directory doesnt exist")
	sys.exit(0)

if os.path.exists(project_dir):
	shutil.rmtree(project_dir)

additional_empty_dirs = []
if os.path.exists(emptydirs_file):		# Only used if names are specified by commandline and not input!
	with open(emptydirs_file) as f:
		for line in f.readlines():
			directory = line.strip()
			if not directory:
				continue

			additional_empty_dirs.append(directory)


for root, dirs, files in os.walk(template_dir):
	for name in dirs:
		directory = os.path.join(project_dir, os.path.join(os.path.relpath(root, template_dir)), name)
		os.makedirs(directory)

for name in additional_empty_dirs:
	directory = os.path.join(project_dir, name)

	if not os.path.exists(directory):
		os.makedirs(directory)
		

uuid_dict = {}
def replace_with_uuid(x):
	global uuid_dict
	num = int(x.group(1))

	if num not in uuid_dict:
		uuid_dict[num] = str(uuid.uuid4()).upper()

	return uuid_dict[num]

for root, dirs, files in os.walk(template_dir):
	for name in files:
		file_name = name.replace("$PROJECTNAME$", project_name)
		in_file = os.path.join(root, name)
		out_file = os.path.join(project_dir, os.path.join(os.path.relpath(root, template_dir)), file_name)

		if in_file == emptydirs_file:
			continue

		with open(in_file) as f:
			content = f.read()

		content = uuid_re.sub(replace_with_uuid, content)
		content = content.replace("$PROJECTNAME$", project_name)

		with open(out_file, "w") as f:
			f.write(content)

print("Successfully created project '{}'".format(project_name))