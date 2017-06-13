# vim: set ft=python:

 

## SVP4 60 fps

 



import vapoursynth as vs 

core = vs.get_core()
core.std.LoadPlugin("/home/tiziano/SVP 4/plugins/libsvpflow1_vs64.so")
core.std.LoadPlugin("/home/tiziano/SVP 4/plugins/libsvpflow2_vs64.so") 

 #vspipe --y4m svp.py -a I=/data/TorrentDownloads/Film/Genius.S01E01.1080p.HEVC.x265-RMTeam.mkv - | ffmpeg -i /data/TorrentDownloads/Film/Genius.S01E01.1080p.HEVC.x265-RMTeam.mkv -i pipe: -map 0:1 -map 1:0 

 


clip = core.ffms2.Source(source = I)
clip = clip.resize.Bicubic(format=vs.YUV420P8) ##convert to YU12 
crop_string = "" 

#resize_string = "core.resize.Bicubic(clip=input, width=1280, height=720, filter_param_a=0, filter_param_b=0.75)"

resize_string = "core.resize.Bicubic(clip=input, filter_param_a=0, filter_param_b=0.75)"

super_params = "{pel:1,scale:{up:0},gpu:0,full:false,rc:true}" ##디폴트gpu=1 (gpu가속사용), 리눅스에서 에러떠서 0(사용안함)으로 변경

analyse_params = "{main:{search:{coarse:{distance:-8},distance:0}}}" 

smoothfps_params = "{rate:{num:5,den:2},algo:13,mask:{area:50},scene:{blend:true}}" ##퀄리티 설정: 24->60fps ...

#smoothfps_params = "{gpuid:11,rate:{num:2,den:1},algo:13,mask:{area:50},scene:{blend:true}}" ##더블 프레임 ex) 24->48fps

 

def interpolate(clip): 

    input = clip 
    if crop_string!='': 
        input = eval(crop_string) 
    if resize_string!='': 
        input = eval(resize_string) 
    super = core.svp1.Super(input,super_params) 
    vectors = core.svp1.Analyse(super["clip"],super["data"],input,analyse_params)
    smooth = core.svp2.SmoothFps(clip,super["clip"],super["data"],vectors["clip"],vectors["data"],smoothfps_params, fps=60)

    smooth = core.std.AssumeFPS(smooth,fpsnum=smooth.fps_num,fpsden=smooth.fps_den)

    return smooth 


smooth = interpolate(clip) 

 

smooth.set_output()
