import os
import subprocess
import xnat

#pip install xnat
#pip install heudiconv

# Connect to XNAT server
xnat_host = 'https://your-xnat-server.com'
xnat_user = 'username'
xnat_password = 'password'
with xnat.connect(xnat_host, user=xnat_user, password=xnat_password) as session:

    # Set the project and subject IDs
    project_id = 'BDV01_CMH'
    subject_id = 'BDV01_CMH_00011007'

    # Get the experiment ID of the imaging data
    experiment_id = session.projects[project_id].subjects[subject_id].experiments[0].id

    # Get the scans of the experiment
    scans = session.select('xnat:mrScanData').where('xnat:mrSessionData.ID={}'.format(experiment_id))

    # Download the scans to a local folder
    output_folder = 'C:/Users/obeyk/Documents/GitHub/xnat2bids/xnat_to_bids.py'
    scans.download(output_folder)

    # Change directory to the downloaded folder
    os.chdir(output_folder)

    # Set up the command for dcm2niix
    dcm2niix_cmd = 'dcm2niix -b y -ba y -z y -f {}_%s -o {} .'.format('sub', output_folder)

    # Run dcm2niix on each DICOM file
    for root, dirs, files in os.walk(output_folder):
        for file in files:
            if file.endswith('.dcm'):
                subprocess.run(dcm2niix_cmd % ('{subject}',), shell=True)

    # Set up the command for Heudiconv
    heudiconv_cmd = 'heudiconv -d ./%s/%s/%s/%s/%s/%s/%s -s %s -f /path/to/conversion/file.py -c dcm2niix -o %s' % ('*', '*', '*', '*', '*', '*', '*', experiment_id, output_folder)

    # Run the Heudiconv command
    subprocess.run(heudiconv_cmd, shell=True)
