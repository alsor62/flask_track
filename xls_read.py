import time
import datetime
import paho.mqtt.client as mqtt
import json
import random

import mqtt_pub




def psictofloat(psic):
    ps = '.'
    pospsic = psic.find(',')
    if pospsic > 0:
        temp = list(psic)
        temp[pospsic] = ps
        pospsic = "".join(temp)
        fpsic = float(pospsic)
    else:
        fpsic = 0

    return fpsic


def read_track():
    # track = pd.read_excel ('track_boot.xlsx')
    # print (track)
    file1 = open("tb1.txt", "r")
    nc = '.'
    fuel_full = 27.3
    m100f = 5.7
    totaldelay = 0
    prog_dist = (fuel_full / m100f) * 100
    print('prg = ', prog_dist)

    lines = 0

    for line in file1:
        lines += 1
    print(lines)
    file1.close()

    broker_address = "116.203.133.211"

    client = mqtt.Client("P1")  # create new instance
    client.connect(broker_address)  # connect to broker
    topic_pub = 'CarOS/Telemetry'

    time.sleep(3)

    file1 = open("tb1.txt", "r")

    while True:
        for line in file1:
            cline = line.strip()
            p1 = cline.find(' ')
            p2 = cline.find(' ', p1 + 1)
            delay = cline[p1:p2]

            p3 = cline.find(' ', p2 + 1)
            pname = cline[p2:p3]

            p4 = cline.find(' ', p3 + 1)
            pval = cline[p3:p4]

            p5 = cline.find(' ', p4 + 1)
            gps_s = cline[p4:p5]

            p6 = cline.find(' ', p5 + 1)
            gps_d = cline[p5:p6]

            fdelay = psictofloat(delay)

            #print('fdelay ', fdelay)

            pn = pname.find('NOP')
            if pn < 0:
                now = datetime.datetime.now()
                # print('curr time ',  now.strftime("%Y-%m-%d %H:%M:%S"))
                # print(fdelay,' name ',pname, 'val ', pval,' gps_s ',gps_s, 'gps_d ', gps_d)
                if pname.find('UFUEL') > 0:

                    ffu = psictofloat(pval)
                    fuel_full = fuel_full - ffu
                    # print('FUEL = ', fuel_full)
                    # time.sleep(3)

                elif pname.find('M100FUEL') > 0:
                    pv1 = pval.find(',')
                    if pv1 > 0:
                        temp1 = list(pval)
                        temp1[pv1] = nc
                        pval = "".join(temp1)
                        m100f = float(pval)

                        # print('NEW 100L = ', m100f)
                        # prog_dist = (fuel_full/m100f)*100

                        # ctr_time = now1.strftime("%Y-%m-%d %H:%M:%S")

                        # pack_mqtt = {'curr_time': ctr_time, 'M100FUEL': m100f, 'PROGDIST': prog_dist,}
                        # print ('prognoz = ',prog_dist)
                        # time.sleep(5)

                elif pname.find('VGPS') > 0:

                    now1 = datetime.datetime.now()

                    ctr_time = now1.strftime("%Y-%m-%d %H:%M:%S")
                    # ctr_time = '33333'

                    if pval == '0':
                        lidar = 9999.99
                    else:
                        lidar = random.uniform(0.3, 4.5)

                    fvgps = psictofloat(pval)
                    fgps_s = psictofloat(gps_s)
                    fgps_d = psictofloat(gps_d)

                    pack_mqtt = {'currentTime': ctr_time, 'gpsVelocity': fvgps, 'latitude': fgps_s, 'longitude': fgps_d, 'm100Fuel': m100f,
                                 'progDistance': prog_dist, 'fuelTank': fuel_full, 'lidarFronLeft': lidar}
                    json_pack = json.dumps(pack_mqtt)
                    print('mqtt = ',pack_mqtt)
                    mqtt_pub.mqtt_pub(client, topic_pub, json_pack)
                else:
                    now1 = datetime.datetime.now()

                    ctr_time = now1.strftime("%Y-%m-%d %H:%M:%S")

                    if pname.find('AXCEL') > 0:
                        nname ='axcel'
                    elif pname.find('DIST') > 0:
                        nname = 'distance'
                    elif pname.find('ENGP') > 0:
                        nname ='engp'
                    elif pname.find('MAFP') > 0:
                        nname ='mafp'
                    elif pname.find('MFUEL') > 0:
                        nname = 'mFuel'
                    elif pname.find('RPM') > 0:
                        nname = 'rpm'
                    elif pname.find('TENG') > 0:
                        nname = 'teng'
                    elif pname.find('UFUEL') > 0:
                        nname = 'uFuel'
                    elif pname.find('VBAT') > 0:
                        nname = 'batteryVoltage'
                    elif pname.find('VODO') > 0:
                        nname = 'odometrVelocity'





                    fpval = psictofloat(pval)
                    pack_mqtt = {'currentTime': ctr_time, nname: fpval, }
                    json_pack = json.dumps(pack_mqtt)
                    print ('mqtt2 =', pack_mqtt)
                    mqtt_pub.mqtt_pub(client, topic_pub, json_pack)






            else:

                now1 = datetime.datetime.now()

                ctr_time = now1.strftime("%Y-%m-%d %H:%M:%S")
                pack_mqtt = {'currentTime': ctr_time, 'climatic1': 18.7, }
                json_pack = json.dumps(pack_mqtt)
                mqtt_pub.mqtt_pub(client, topic_pub, json_pack)

                print('climaic = ', pack_mqtt)

            if fdelay > 0:
                totaldelay = totaldelay + fdelay
                print('total delay = ',totaldelay)
                time.sleep(fdelay)

        file1.close
        print('ddd')
        break
