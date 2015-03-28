import os
import sys
import shutil
import uuid
import re

# Configuration:
template_dir_name = "VS2013"
additional_empty_dirs = ["bin", "build", "include", "run", "lib/x64", "lib/x86"]
# This is neccessary because you cant push empty dirs in git.
# But if you use it on your local computer you can just create empty directorys in your template folder!

if len(sys.argv) != 2:
	print("Usage: " + os.path.basename(__file__) + " [PROJECT NAME]")
	sys.exit(0)

project_name = sys.argv[1].strip()


uuid_re = re.compile(r"\{\$UUID_([0-9]+)\$\}")

if project_name == template_dir_name:
	print("Project name cannot be the same as template directory name")
	sys.exit(0)

working_dir = os.path.dirname(os.path.realpath(__file__))
project_dir = os.path.join(os.getcwd(), project_name)
template_dir = os.path.join(working_dir, template_dir_name)

if os.path.exists(project_dir):
	shutil.rmtree(project_dir)


for root, dirs, files in os.walk(template_dir):
	for name in dirs:
		directory = os.path.join(project_dir, os.path.join(os.path.relpath(root, template_dir)), name)
		os.makedirs(directory)

for name in additional_empty_dirs:
	directory = os.path.join(project_dir, name)

	if not os.path.exists(directory):
		os.makedirs(directory)
		

uuid_dict = {}

for root, dirs, files in os.walk(template_dir):
	for name in files:
		file_name = name.replace("$PROJECTNAME$", project_name)
		in_file = os.path.join(root, name)
		out_file = os.path.join(project_dir, os.path.join(os.path.relpath(root, template_dir)), file_name)

		with open(in_file) as f:
			content = f.read()

		def replace_with_uuid(x):
			global uuid_dict
			num = int(x.group(1))

			if num not in uuid_dict:
				uuid_dict[num] = str(uuid.uuid4()).upper()

			return uuid_dict[num]

		content = uuid_re.sub(replace_with_uuid, content)
		content = content.replace("$PROJECTNAME$", project_name)

		with open(out_file, "w") as f:
			f.write(content)

print("Successfully created project '{}'".format(project_name))