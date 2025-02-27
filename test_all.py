import os
import pygreat
import datetime

if __name__ == "__main__":
    top_dir = os.getcwd()
    msf_dir = os.path.join(top_dir, "MSF_20201027")
    os.chdir(msf_dir)
    gset = pygreat.GCFG_IGN()
    gset.app(
        "GREAT-MSF",
        "1.0.0",
        "$Rev: 2448 $",
        "(@whu,edu,cn)",
        datetime.datetime.now().strftime("%Y-%m-%d"),
        datetime.datetime.now().strftime("%H:%M:%S"),
    )
    gset.arg("xml/GREAT_MSF_LCPPP_1027_campus_01.xml")
    log_type = gset.log_type()
    log_level = gset.log_level()
    log_name = gset.log_name()
    log_pattern = gset.log_pattern()
    pygreat.set_level(log_level)
    pygreat.set_pattern(log_pattern, pygreat.pattern_time_type.local)
    pygreat.flush_on(pygreat.LogLevel.err)
    great_log = pygreat.GRTLog(log_type, log_level, log_name)
    my_logger = great_log.spdlog()
    isBase = False
    if gset.list_base():
        isBase = True
    sites = gset.recs()
    sample = int(gset.sampling())
    if not sample:
        sample = int(gset.sampling_default())
    beg = gset.beg()
    end = gset.end()
    filepackage = pygreat.readfilepackage(gset, my_logger, isBase, beg)
    data = filepackage["data"]
    gobs = filepackage["gobs"]
    gupd = filepackage["gupd"]
    gimu = filepackage["gimu"]
    # todo current time
    i = 0
    nsite = sites.__len__()
    if isBase:
        nsite = gset.list_rover().__len__()
    it = iter(sites)
    LAST_TIME = pygreat.get_LAST_TIME()
    FIRST_TIME = pygreat.get_FIRST_TIME()
    site = next(it)
    vgmsf: [pygreat.GIntegration] = []
    while i < nsite:
        site_base = ""
        if isBase:
            site_base = gset.list_base()[i]
            site = gset.list_rover()[i]
            if (
                (gobs.beg_obs(site_base,0) == LAST_TIME)
                or (gobs.end_obs(site_base) == LAST_TIME)
                or (site_base == "")
                or (gobs.isSite(site_base) == False)
            ):
                # todo log
                i += 1
                continue
        if (
            (gobs.beg_obs(site, 0) == LAST_TIME)
            or (gobs.end_obs(site) == LAST_TIME)
            or (site == "")
            or (gobs.isSite(site) == False)
        ):
            # todo log
            i += 1
            continue
        vgmsf.append(0)  # 在列表末尾添加 0
        idx = len(vgmsf) - 1  # 获取列表的最后一个索引
        vgmsf[idx] = pygreat.GIntegration(site, site_base, gset, my_logger, data)
        if gset.fix_mode() != pygreat.FIX_MODE.NO and not isBase:
            vgmsf[idx].ADD_UPD(gupd)
        vgmsf[idx].Add_IMU(gimu)
        # todo log
        # todo log
        # todo runtime
        vgmsf[idx].processBatchFB(beg, end, True)
        # todo lstepoch
        # todo log
        if not isBase and sites.__len__() > 1:
            site = next(it)
        i += 1
