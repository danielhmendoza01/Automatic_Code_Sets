# Define the source paths and destination path
$source1 = "C:\Users\Daniel\Documents\opiod_list\Atomatic_Code_Sets\RxNorm\Opioid"
$source2 = "C:\Users\Daniel\Documents\opiod_list\Atomatic_Code_Sets\RxNorm\Antidepressant"
$destination = "C:\Users\Daniel\Documents\opiod_list\Atomatic_Code_Sets\RxNorm\Appendices"
# Define the file names
$fileNames = "New_Complete_Opioids_List.xlsx", "Same_Opioid_Medications.xlsx", "New_Opioids_Added.xlsx", "Obsolete_Not_Found.xlsx", "Active_Not_Found.xlsx", "New_Complete_Antidepressants_List.xlsx", "Same_Antidepressant_Medications.xlsx", "New_Antidepressant_Added.xlsx","Active_Not_Found_Antidepressant.xlsx"

# Use a for loop to iterate over the array of file names
for ($i = 0; $i -lt $fileNames.Length; $i++) {
  # Set the file name and new file name
  $file = $fileNames[$i]
  $newName = "Appendix" + ($i + 3) + ".xlsx"

  # Set the source path based on the index of the file
  if ($i -lt 5) {
    $source = $source1
  }
  else {
    $source = $source2
  }

  # Copy the file to the destination folder
  Copy-Item "$source\$file" $destination

  # Change the name of the copied file
  Rename-Item "$destination\$file" $newName
}
