import os, json, pydicom

folder = "images/1a6cffc7270de465a1d023417ad872ae5d29b05d072e3dfdd431d87b"
base_url = "https://rosewarnedm.github.io/CTB_education/images/1a6cffc7270de465a1d023417ad872ae5d29b05d072e3dfdd431d87b"
output_json = "study.json"

instances = []

for f in os.listdir(folder):
    if not f.lower().endswith(".dcm"):
        continue
    ds = pydicom.dcmread(os.path.join(folder, f), stop_before_pixels=True)
    instances.append({
        "SOPInstanceUID": ds.SOPInstanceUID,
        "InstanceNumber": getattr(ds, "InstanceNumber", 0),
        "url": f"{base_url}/{f}"
    })

# sort by InstanceNumber
instances.sort(key=lambda x: x["InstanceNumber"])

study_json = {
    "studies": [
        {
            "StudyInstanceUID": ds.StudyInstanceUID,
            "Series": [
                {
                    "SeriesInstanceUID": ds.SeriesInstanceUID,
                    "Instances": [{"SOPInstanceUID": i["SOPInstanceUID"], "url": i["url"]} for i in instances]
                }
            ]
        }
    ]
}

with open(os.path.join(folder, output_json), "w") as f:
    json.dump(study_json, f, indent=2)

print(f"✅ Generated {output_json} with sorted instances")
