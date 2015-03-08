import os
import sys
import shutil

if len(sys.argv) != 2:
	print("Usage: " + os.path.basename(__file__) + " [PROJECT NAME]")
	sys.exit(0)

project_name = sys.argv[1].strip()

working_dir = os.path.dirname(os.path.realpath(__file__))
project_dir = os.path.join(os.getcwd(), project_name)
template_dir = os.path.join(working_dir, "template")

if os.path.exists(project_dir):
	shutil.rmtree(project_dir)


for root, dirs, files in os.walk(template_dir):
	for name in dirs:
		os.makedirs(os.path.join(project_dir, os.path.join(os.path.relpath(root, template_dir)), name))

for root, dirs, files in os.walk(template_dir):
	for name in files:
		file_name = name.replace("$PROJECTNAME$", project_name)
		in_file = os.path.join(root, name)
		out_file = os.path.join(project_dir, os.path.join(os.path.relpath(root, template_dir)), file_name)

		open(out_file, "w").write(open(in_file).read().replace("$PROJECTNAME$", project_name))

print("Successfully created project '{}'".format(project_name))