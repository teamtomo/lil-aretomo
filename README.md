# lil_aretomo

im not a (w)rapper

see the script in example directory for the kind of input script you need to run this.

    Parameters
    ----------

    tilt_series_file: file containing tilt-series images
    tilt_angles: nominal stage tilt-angles from the microscope.
    pixel_size: pixel size of the tilt-series in angstroms-per-pixel
    output_directory: tilt-series directory for IMOD.
    exe: path to the AreTomo executable file
    (optional) local_align: carry out local tilt series alignments? Yes or no, default is no
    (optional) target_pixel_size: the ideal pixel size at which TSA is carried out. Default is 10A
    (optional) nominal_rotation_angle: initial estimate for the rotation angle of the tilt
    axis. AreTomo does not need this information but it might help.
    (optional) patch_in_x: if local_align is True, AreTomo will carry out patch tracking.
    Specify the number of patches in X here. Default is 5.
    (optional) patch_in_y: same as above, but in Y. Default is 4.
    (optional) correct_tilt_angle_offset: Apply tilt angle offset correction, yes or no.
    Default is no. See AreTomo manual for full explanation: yes adds the -TiltCor 1 argument.
