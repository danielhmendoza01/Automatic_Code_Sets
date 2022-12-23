# Define the source and destination paths
$file = "active.xlsx"
$source = "C:\Users\Daniel\Documents\opiod_list\Atomatic_Code_Sets\NDC\Antidepressants\$file"
$destination = "C:\Users\Daniel\Dropbox (ASU)\RxNorm Opioids\NDC\NDC Paper\Appendices"

# Copy the file to the destination folder
Copy-Item $source $destination

# Define the new name for the file
$newName = "Appendix14.xlsx"

# Change the name of the copied file
Rename-Item "$destination\$file" $newName
