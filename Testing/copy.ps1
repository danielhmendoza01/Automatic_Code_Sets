# Define the source paths and destination path
$source1 = "C:\Users\Daniel\Documents\opiod_list\Atomatic_Code_Sets\NDC\Opioids"
$source2 = "C:\Users\Daniel\Documents\opiod_list\Atomatic_Code_Sets\NDC\Antidepressants"
$destination = "C:\Users\Daniel\Dropbox (ASU)\RxNorm Opioids\NDC\NDC Paper\Appendices"

# Define the file names
$fileNames = "ndc_opioids.xlsx", "Same_Opioid_Medications.xlsx", "New_Opioids_Added.xlsx", "Absent_Opioid.xlsx", "NOT_active.xlsx", "active.xlsx", "ndc_antidepressants.xlsx", "Same_Antidepressants_Medications.xlsx", "New_antidepressants_Added.xlsx", "Absent_Antidepressants.xlsx", "NOT_active.xlsx", "active.xlsx", "error.xlsx"

# Use a for loop to iterate over the array of file names
for ($i = 0; $i -lt $fileNames.Length; $i++) {
  # Set the file name and new file name
  $file = $fileNames[$i]
  $newName = "Appendix" + ($i + 3) + ".xlsx"

  # Set the source path based on the index of the file
  if ($i -lt 6) {
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
