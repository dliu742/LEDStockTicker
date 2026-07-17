import time
import threading
import argparse
import traceback
import numpy as np
import pandas as pd
import pytz
from datetime import datetime
import requests
import yfinance as yf
from rpi_ws281x import Adafruit_NeoPixel, Color
from flask import Flask, render_template_string, request, jsonify
from PIL import Image, ImageDraw

# --- 1. LED STRIP CONFIGURATION ---
LED_COUNT = 1280       
LED_PIN = 18           
LED_FREQ_HZ = 800000   
LED_DMA = 10           
LED_INVERT = False     
LED_CHANNEL = 0        
LED_BRIGHTNESS = 15

ledWidth = 40
ledHeight = 32

# User's Matrix Mapping
ledMappingMatrix = np.array([
    [255,254,253,252,251,250,249,248,263,262,261,260,259,258,257,256,767,766,765,764,763,762,761,760,775,774,773,772,771,770,769,768,1279,1278,1277,1276,1275,1274,1273,1272],
    [240,241,242,243,244,245,246,247,264,265,266,267,268,269,270,271,752,753,754,755,756,757,758,759,776,777,778,779,780,781,782,783,1264,1265,1266,1267,1268,1269,1270,1271],
    [239,238,237,236,235,234,233,232,279,278,277,276,275,274,273,272,751,750,749,748,747,746,745,744,791,790,789,788,787,786,785,784,1263,1262,1261,1260,1259,1258,1257,1256],
    [224,225,226,227,228,229,230,231,280,281,282,283,284,285,286,287,736,737,738,739,740,741,742,743,792,793,794,795,796,797,798,799,1248,1249,1250,1251,1252,1253,1254,1255],
    [223,222,221,220,219,218,217,216,295,294,293,292,291,290,289,288,735,734,733,732,731,730,729,728,807,806,805,804,803,802,801,800,1247,1246,1245,1244,1243,1242,1241,1240],
    [208,209,210,211,212,213,214,215,296,297,298,299,300,301,302,303,720,721,722,723,724,725,726,727,808,809,810,811,812,813,814,815,1232,1233,1234,1235,1236,1237,1238,1239],
    [207,206,205,204,203,202,201,200,311,310,309,308,307,306,305,304,719,718,717,716,715,714,713,712,823,822,821,820,819,818,817,816,1231,1230,1229,1228,1227,1226,1225,1224],
    [192,193,194,195,196,197,198,199,312,313,314,315,316,317,318,319,704,705,706,707,708,709,710,711,824,825,826,827,828,829,830,831,1216,1217,1218,1219,1220,1221,1222,1223],
    [191,190,189,188,187,186,185,184,327,326,325,324,323,322,321,320,703,702,701,700,699,698,697,696,839,838,837,836,835,834,833,832,1215,1214,1213,1212,1211,1210,1209,1208],
    [176,177,178,179,180,181,182,183,328,329,330,331,332,333,334,335,688,689,690,691,692,693,694,695,840,841,842,843,844,845,846,847,1200,1201,1202,1203,1204,1205,1206,1207],
    [175,174,173,172,171,170,169,168,343,342,341,340,339,338,337,336,687,686,685,684,683,682,681,680,855,854,853,852,851,850,849,848,1199,1198,1197,1196,1195,1194,1193,1192],
    [160,161,162,163,164,165,166,167,344,345,346,347,348,349,350,351,672,673,674,675,676,677,678,679,856,857,858,859,860,861,862,863,1184,1185,1186,1187,1188,1189,1190,1191],
    [159,158,157,156,155,154,153,152,359,358,357,356,355,354,353,352,671,670,669,668,667,666,665,664,871,870,869,868,867,866,865,864,1183,1182,1181,1180,1179,1178,1177,1176],
    [144,145,146,147,148,149,150,151,360,361,362,363,364,365,366,367,656,657,658,659,660,661,662,663,872,873,874,875,876,877,878,879,1168,1169,1170,1171,1172,1173,1174,1175],
    [143,142,141,140,139,138,137,136,375,374,373,372,371,370,369,368,655,654,653,652,651,650,649,648,887,886,885,884,883,882,881,880,1167,1166,1165,1164,1163,1162,1161,1160],
    [128,129,130,131,132,133,134,135,376,377,378,379,380,381,382,383,640,641,642,643,644,645,646,647,888,889,890,891,892,893,894,895,1152,1153,1154,1155,1156,1157,1158,1159],
    [127,126,125,124,123,122,121,120,391,390,389,388,387,386,385,384,639,638,637,636,635,634,633,632,903,902,901,900,899,898,897,896,1151,1150,1149,1148,1147,1146,1145,1144],
    [112,113,114,115,116,117,118,119,392,393,394,395,396,397,398,399,624,625,626,627,628,629,630,631,904,905,906,907,908,909,910,911,1136,1137,1138,1139,1140,1141,1142,1143],
    [111,110,109,108,107,106,105,104,407,406,405,404,403,402,401,400,623,622,621,620,619,618,617,616,919,918,917,916,915,914,913,912,1135,1134,1133,1132,1131,1130,1129,1128],
    [96,97,98,99,100,101,102,103,408,409,410,411,412,413,414,415,608,609,610,611,612,613,614,615,920,921,922,923,924,925,926,927,1120,1121,1122,1123,1124,1125,1126,1127],
    [95,94,93,92,91,90,89,88,423,422,421,420,419,418,417,416,607,606,605,604,603,602,601,600,935,934,933,932,931,930,929,928,1119,1118,1117,1116,1115,1114,1113,1112],
    [80,81,82,83,84,85,86,87,424,425,426,427,428,429,430,431,592,593,594,595,596,597,598,599,936,937,938,939,940,941,942,943,1104,1105,1106,1107,1108,1109,1110,1111],
    [79,78,77,76,75,74,73,72,439,438,437,436,435,434,433,432,591,590,589,588,587,586,585,584,951,950,949,948,947,946,945,944,1103,1102,1101,1100,1099,1098,1097,1096],
    [64,65,66,67,68,69,70,71,440,441,442,443,444,445,446,447,576,577,578,579,580,581,582,583,952,953,954,955,956,957,958,959,1088,1089,1090,1091,1092,1093,1094,1095],
    [63,62,61,60,59,58,57,56,455,454,453,452,451,450,449,448,575,574,573,572,571,570,569,568,967,966,965,964,963,962,961,960,1087,1086,1085,1084,1083,1082,1081,1080],
    [48,49,50,51,52,53,54,55,456,457,458,459,460,461,462,463,560,561,562,563,564,565,566,567,968,969,970,971,972,973,974,975,1072,1073,1074,1075,1076,1077,1078,1079],
    [47,46,45,44,43,42,41,40,471,470,469,468,467,466,465,464,559,558,557,556,555,554,553,552,983,982,981,980,979,978,977,976,1071,1070,1069,1068,1067,1066,1065,1064],
    [32,33,34,35,36,37,38,39,472,473,474,475,476,477,478,479,544,545,546,547,548,549,550,551,984,985,986,987,988,989,990,991,1056,1057,1058,1059,1060,1061,1062,1063],
    [31,30,29,28,27,26,25,24,487,486,485,484,483,482,481,480,543,542,541,540,539,538,537,536,999,998,997,996,995,994,993,992,1055,1054,1053,1052,1051,1050,1049,1048],
    [16,17,18,19,20,21,22,23,488,489,490,491,492,493,494,495,528,529,530,531,532,533,534,535,1000,1001,1002,1003,1004,1005,1006,1007,1040,1041,1042,1043,1044,1045,1046,1047],
    [15,14,13,12,11,10,9,8,503,502,501,500,499,498,497,496,527,526,525,524,523,522,521,520,1015,1014,1013,1012,1011,1010,1009,1008,1039,1038,1037,1036,1035,1034,1033,1032],
    [0,1,2,3,4,5,6,7,504,505,506,507,508,509,510,511,512,513,514,515,516,517,518,519,1016,1017,1018,1019,1020,1021,1022,1023,1024,1025,1026,1027,1028,1029,1030,1031]
])

# --- 2. CUSTOM FONT DICTIONARY ---
# Integrating the user's provided NumPy array dictionary mapping
CUSTOM_FONT = {
    ' ': np.array([[0],[0],[0],[0],[0],[0],[0],[0],[0],[0]]),
    '.': np.array([[0],[0],[0],[0],[0],[0],[0],[0],[0],[1]]),
    'A': np.array([[0, 1, 1, 0],[1, 1, 1, 1],[1, 0, 0, 1],[1, 0, 0, 1],[1, 0, 0, 1],[1, 1, 1, 1],[1, 1, 1, 1],[1, 0, 0, 1],[1, 0, 0, 1],[1, 0, 0, 1]]),
    'B': np.array([[1, 1, 1, 0],[1, 0, 0, 1],[1, 0, 0, 1],[1, 0, 0, 1],[1, 1, 1, 0],[1, 1, 1, 0],[1, 0, 0, 1],[1, 0, 0, 1],[1, 0, 0, 1],[1, 1, 1, 0]]),
    'C': np.array([[0, 1, 1, 0],[1, 1, 1, 1],[1, 0, 0, 1],[1, 0, 0, 0],[1, 0, 0, 0],[1, 0, 0, 0],[1, 0, 0, 0],[1, 0, 0, 1],[1, 1, 1, 1],[0, 1, 1, 0]]),
    'D': np.array([[1, 1, 0, 0],[1, 1, 1, 0],[1, 0, 1, 1],[1, 0, 0, 1],[1, 0, 0, 1],[1, 0, 0, 1],[1, 0, 0, 1],[1, 0, 1, 1],[1, 1, 1, 0],[1, 1, 0, 0]]),
    'E': np.array([[1, 1, 1, 1],[1, 1, 1, 1],[1, 0, 0, 0],[1, 0, 0, 0],[1, 1, 1, 0],[1, 1, 1, 0],[1, 0, 0, 0],[1, 0, 0, 0],[1, 1, 1, 1],[1, 1, 1, 1]]),
    'F': np.array([[1, 1, 1, 1],[1, 1, 1, 1],[1, 0, 0, 0],[1, 0, 0, 0],[1, 1, 1, 0],[1, 1, 1, 0],[1, 0, 0, 0],[1, 0, 0, 0],[1, 0, 0, 0],[1, 0, 0, 0]]),
    'G': np.array([[0, 1, 1, 0],[1, 1, 1, 1],[1, 0, 0, 1],[1, 0, 0, 0],[1, 0, 0, 0],[1, 0, 1, 1],[1, 0, 0, 1],[1, 0, 0, 1],[1, 1, 1, 1],[0, 1, 1, 0]]),
    'H': np.array([[1, 0, 0, 1],[1, 0, 0, 1],[1, 0, 0, 1],[1, 0, 0, 1],[1, 1, 1, 1],[1, 1, 1, 1],[1, 0, 0, 1],[1, 0, 0, 1],[1, 0, 0, 1],[1, 0, 0, 1]]),
    'I': np.array([[0, 1, 1, 1],[0, 0, 1, 0],[0, 0, 1, 0],[0, 0, 1, 0],[0, 0, 1, 0],[0, 0, 1, 0],[0, 0, 1, 0],[0, 0, 1, 0],[0, 0, 1, 0],[0, 1, 1, 1]]),
    'J': np.array([[1, 1, 1, 1],[1, 1, 1, 1],[0, 0, 1, 0],[0, 0, 1, 0],[0, 0, 1, 0],[0, 0, 1, 0],[1, 0, 1, 0],[1, 0, 1, 0],[1, 1, 1, 0],[0, 1, 0, 0]]),
    'K': np.array([[1, 0, 0, 1],[1, 0, 0, 1],[1, 0, 1, 0],[1, 1, 1, 0],[1, 1, 0, 0],[1, 1, 0, 0],[1, 0, 1, 0],[1, 0, 1, 0],[1, 0, 0, 1],[1, 0, 0, 1]]),
    'L': np.array([[1, 0, 0, 0],[1, 0, 0, 0],[1, 0, 0, 0],[1, 0, 0, 0],[1, 0, 0, 0],[1, 0, 0, 0],[1, 0, 0, 0],[1, 0, 0, 0],[1, 0, 0, 0],[1, 1, 1, 1]]),
    'M': np.array([[1, 0, 0, 1],[1, 1, 1, 1],[1, 1, 1, 1],[1, 1, 1, 1],[1, 1, 0, 1],[1, 0, 0, 1],[1, 0, 0, 1],[1, 0, 0, 1],[1, 0, 0, 1],[1, 0, 0, 1]]),
    'N': np.array([[1, 0, 0, 1],[1, 0, 0, 1],[1, 1, 0, 1],[1, 1, 0, 1],[1, 1, 0, 1],[1, 0, 1, 1],[1, 0, 1, 1],[1, 0, 1, 1],[1, 0, 0, 1],[1, 0, 0, 1]]),
    'O': np.array([[0, 1, 1, 0],[1, 1, 1, 1],[1, 0, 0, 1],[1, 0, 0, 1],[1, 0, 0, 1],[1, 0, 0, 1],[1, 0, 0, 1],[1, 0, 0, 1],[1, 1, 1, 1],[0, 1, 1, 0]]),
    'P': np.array([[0, 1, 1, 0],[1, 0, 1, 1],[1, 0, 0, 1],[1, 0, 0, 1],[1, 0, 1, 1],[1, 1, 1, 0],[1, 0, 0, 0],[1, 0, 0, 0],[1, 0, 0, 0],[1, 0, 0, 0]]),
    'Q': np.array([[0, 1, 1, 0],[1, 1, 1, 1],[1, 0, 0, 1],[1, 0, 0, 1],[1, 0, 0, 1],[1, 0, 0, 1],[1, 0, 0, 1],[1, 0, 1, 0],[1, 1, 1, 1],[0, 1, 0, 1]]),
    'R': np.array([[0, 1, 1, 0],[1, 1, 1, 1],[1, 0, 0, 1],[1, 0, 0, 1],[1, 0, 0, 1],[1, 1, 1, 1],[1, 0, 1, 0],[1, 0, 1, 0],[1, 0, 0, 1],[1, 0, 0, 1]]),
    'S': np.array([[0, 1, 1, 0],[1, 1, 1, 1],[1, 0, 0, 1],[1, 0, 0, 0],[1, 1, 0, 0],[0, 1, 1, 1],[0, 0, 0, 1],[1, 0, 0, 1],[1, 1, 1, 1],[0, 1, 1, 0]]),
    'T': np.array([[0, 1, 1, 1],[0, 0, 1, 0],[0, 0, 1, 0],[0, 0, 1, 0],[0, 0, 1, 0],[0, 0, 1, 0],[0, 0, 1, 0],[0, 0, 1, 0],[0, 0, 1, 0],[0, 0, 1, 0]]),
    'U': np.array([[1, 0, 0, 1],[1, 0, 0, 1],[1, 0, 0, 1],[1, 0, 0, 1],[1, 0, 0, 1],[1, 0, 0, 1],[1, 0, 0, 1],[1, 0, 0, 1],[1, 1, 1, 1],[0, 1, 1, 0]]),
    'V': np.array([[1, 0, 0, 1],[1, 0, 0, 1],[1, 0, 0, 1],[1, 0, 0, 1],[1, 0, 0, 1],[1, 0, 0, 1],[1, 0, 0, 1],[1, 0, 0, 1],[1, 0, 0, 1],[0, 1, 1, 0]]),
    'W': np.array([[1, 0, 0, 1],[1, 0, 0, 1],[1, 0, 0, 1],[1, 0, 0, 1],[1, 0, 0, 1],[1, 0, 0, 1],[1, 1, 0, 1],[1, 1, 1, 1],[1, 1, 1, 1],[0, 1, 1, 0]]),
    'X': np.array([[1, 0, 0, 1],[1, 0, 0, 1],[1, 0, 0, 1],[1, 0, 0, 1],[0, 1, 1, 0],[0, 1, 1, 0],[1, 0, 0, 1],[1, 0, 0, 1],[1, 0, 0, 1],[1, 0, 0, 1]]),
    'Y': np.array([[0, 1, 0, 1],[0, 1, 0, 1],[0, 1, 0, 1],[0, 1, 0, 1],[0, 1, 1, 1],[0, 0, 1, 0],[0, 0, 1, 0],[0, 0, 1, 0],[0, 0, 1, 0],[0, 0, 1, 0]]),
    'Z': np.array([[1, 1, 1, 1],[0, 0, 0, 1],[0, 0, 1, 0],[0, 0, 1, 0],[0, 1, 1, 0],[0, 1, 0, 0],[0, 1, 0, 0],[1, 0, 0, 0],[1, 0, 0, 0],[1, 1, 1, 1]]),
    '0': np.array([[0, 1, 1, 0],[1, 0, 0, 1],[1, 0, 0, 1],[1, 0, 0, 1],[1, 0, 0, 1],[1, 0, 0, 1],[1, 0, 0, 1],[1, 0, 0, 1],[1, 0, 0, 1],[0, 1, 1, 0]]),
    '1': np.array([[0, 1, 1, 0],[1, 0, 1, 0],[0, 0, 1, 0],[0, 0, 1, 0],[0, 0, 1, 0],[0, 0, 1, 0],[0, 0, 1, 0],[0, 0, 1, 0],[0, 0, 1, 0],[1, 1, 1, 1]]),
    '2': np.array([[0, 1, 1, 0],[1, 1, 1, 1],[1, 0, 0, 1],[0, 0, 0, 1],[0, 0, 0, 1],[0, 0, 1, 1],[0, 1, 1, 0],[1, 1, 0, 0],[1, 0, 0, 0],[1, 1, 1, 1]]),
    '3': np.array([[0, 1, 1, 0],[1, 1, 1, 1],[1, 0, 0, 1],[0, 0, 0, 1],[0, 0, 0, 1],[0, 1, 1, 0],[0, 0, 0, 1],[1, 0, 0, 1],[1, 1, 1, 1],[0, 1, 1, 0]]),
    '4': np.array([[0, 0, 1, 0],[0, 1, 1, 0],[0, 1, 1, 0],[1, 0, 1, 0],[1, 0, 1, 0],[1, 1, 1, 1],[0, 0, 1, 0],[0, 0, 1, 0],[0, 0, 1, 0],[0, 0, 1, 0]]),
    '5': np.array([[1, 1, 1, 1],[1, 0, 0, 0],[1, 0, 0, 0],[1, 0, 0, 0],[1, 1, 1, 1],[0, 0, 0, 1],[0, 0, 0, 1],[1, 0, 0, 1],[1, 0, 0, 1],[0, 1, 1, 0]]),
    '6': np.array([[1, 1, 1, 1],[1, 0, 0, 0],[1, 0, 0, 0],[1, 0, 0, 0],[1, 1, 1, 1],[1, 0, 0, 1],[1, 0, 0, 1],[1, 0, 0, 1],[1, 0, 0, 1],[0, 1, 1, 0]]),
    '7': np.array([[1, 1, 1, 1],[0, 0, 0, 1],[0, 0, 0, 1],[0, 0, 0, 1],[0, 0, 0, 1],[0, 0, 0, 1],[0, 0, 0, 1],[0, 0, 0, 1],[0, 0, 0, 1],[0, 0, 0, 1]]),
    '8': np.array([[0, 1, 1, 0],[1, 0, 0, 1],[1, 0, 0, 1],[1, 0, 0, 1],[0, 1, 1, 0],[1, 0, 0, 1],[1, 0, 0, 1],[1, 0, 0, 1],[1, 0, 0, 1],[0, 1, 1, 0]]),
    '9': np.array([[0, 1, 1, 0],[1, 0, 0, 1],[1, 0, 0, 1],[1, 0, 0, 1],[0, 1, 1, 1],[0, 0, 0, 1],[0, 0, 0, 1],[0, 0, 0, 1],[1, 0, 0, 1],[0, 1, 1, 0]]),
    '-': np.array([[0, 0, 0, 0],[0, 0, 0, 0],[0, 0, 0, 0],[0, 0, 0, 0],[1, 1, 1, 1],[1, 1, 1, 1],[0, 0, 0, 0],[0, 0, 0, 0],[0, 0, 0, 0],[0, 0, 0, 0]]),
    ':': np.array([[0],[0],[1],[1],[0],[0],[1],[1],[0],[0]]), # Added colon for time format
    'UP': np.array([[0,0,0],[0,0,0],[0,0,0],[0,1,0],[0,1,0],[1,1,1],[0,1,0],[0,1,0],[0,0,0],[0,0,0]]),
    'DOWN': np.array([[0,0,0],[0,0,0],[0,0,0],[0,0,0],[1,1,1],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]])
}

# --- 3. GLOBAL STATE FOR WEB UI CONTROL ---
state = {
    "is_on": True,
    "mode": "time_weather", 
    "color": [255, 255, 255],
    "brightness": 15,
    "tickers": ["AAPL", "MSFT"],
    "rainbow_colors": [[255, 0, 0], [255, 140, 0], [255, 255, 0], [0, 200, 0], [0, 100, 255], [140, 0, 255]],
    "rainbow_pattern": "wave",   # "wave" (scrolls across the panel) or "cycle" (whole panel fades through the list)
    "rainbow_speed": 5           # 1 (slow) - 10 (fast)
}

# --- 4. FLASK WEB SERVER SETUP ---
app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>LED Matrix Controller</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 2rem; background: #222; color: #eee; }
        .container { max-width: 600px; margin: auto; background: #333; padding: 2rem; border-radius: 10px; }
        h1 { text-align: center; }
        .control-group { margin-bottom: 1.5rem; }
        label { display: block; font-weight: bold; margin-bottom: 0.5rem; }
        input[type="color"] { width: 100%; height: 40px; border: none; }
        input[type="range"] { width: 100%; }
        button { padding: 10px 15px; border: none; border-radius: 5px; cursor: pointer; background: #555; color: white; margin-right: 5px; }
        button:hover { background: #777; }
        .mode-btn.active { background: #007bff; }
        .power-btn.active-on { background: #28a745; box-shadow: 0 0 0 2px #7be396; }
        .power-btn.active-off { background: #dc3545; box-shadow: 0 0 0 2px #ff8a94; }
        #ticker-list { list-style: none; padding: 0; }
        #ticker-list li { background: #444; padding: 5px; margin-bottom: 5px; display: flex; justify-content: space-between;}
    </style>
</head>
<body>
    <div class="container">
        <h1>Matrix Controller</h1>
        
        <div class="control-group">
            <button class="power-btn" id="btn_power_on" onclick="togglePower(true)">Turn ON</button>
            <button class="power-btn" id="btn_power_off" onclick="togglePower(false)">Turn OFF</button>
        </div>

        <div class="control-group">
            <label>Mode Selection</label>
            <button class="mode-btn" id="btn_light_panel" onclick="setMode('light_panel')">Light Panel</button>
            <button class="mode-btn" id="btn_time_weather" onclick="setMode('time_weather')">Time & Weather</button>
            <button class="mode-btn" id="btn_stock_trading" onclick="setMode('stock_trading')">Stock Trading</button>
            <button class="mode-btn" id="btn_rainbow" onclick="setMode('rainbow')">Rainbow</button>
        </div>

        <div class="control-group">
            <label>Brightness</label>
            <div style="display:flex; align-items:center; gap:10px;">
                <button onclick="stepBrightness(-1)" style="padding:5px 12px;">&#9660;</button>
                <input type="range" id="brightness" min="0" max="255" value="15" oninput="document.getElementById('brightnessValue').textContent = this.value" onchange="updateState()" style="flex:1;">
                <button onclick="stepBrightness(1)" style="padding:5px 12px;">&#9650;</button>
                <span id="brightnessValue" style="min-width:2.5em; text-align:right; font-weight:bold;">15</span>
            </div>
        </div>

        <div class="control-group">
            <label>Panel Color (For Light Panel Mode)</label>
            <input type="color" id="colorPicker" value="#ffffff" onchange="updateState()">
        </div>

        <div class="control-group">
            <label>Stock Tickers (Trading Mode)</label>
            <input type="text" id="newTicker" placeholder="e.g. TSLA" style="padding: 5px;">
            <button onclick="addTicker()">Add</button>
            <ul id="ticker-list"></ul>
        </div>

        <div class="control-group">
            <label>Rainbow Settings</label>

            <div style="margin-bottom:0.75rem;">
                <label style="font-weight:normal; margin-bottom:0.25rem;">Pattern</label>
                <select id="rainbowPattern" onchange="updateRainbowSettings()" style="width:100%; padding:6px;">
                    <option value="wave">Scrolling Wave (colors sweep across the panel)</option>
                    <option value="cycle">Color Cycle (whole panel fades through the list)</option>
                </select>
            </div>

            <div style="margin-bottom:0.75rem;">
                <label style="font-weight:normal; margin-bottom:0.25rem;">Speed</label>
                <input type="range" id="rainbowSpeed" min="1" max="10" value="5" oninput="document.getElementById('rainbowSpeedValue').textContent = this.value" onchange="updateRainbowSettings()">
                <span id="rainbowSpeedValue">5</span>
            </div>

            <div>
                <label style="font-weight:normal; margin-bottom:0.25rem;">Colors (in scroll/cycle order)</label>
                <input type="color" id="newRainbowColor" value="#ff0000" style="width:60px; height:35px; vertical-align:middle;">
                <button onclick="addRainbowColor()">Add Color</button>
                <ul id="rainbow-color-list"></ul>
            </div>
        </div>
    </div>

    <script>
        let state = {
            is_on: true,
            mode: "light_panel",
            color: [255, 255, 255],
            brightness: 15,
            tickers: ["AAPL", "MSFT"],
            rainbow_colors: [[255, 0, 0], [255, 140, 0], [255, 255, 0], [0, 200, 0], [0, 100, 255], [140, 0, 255]],
            rainbow_pattern: "wave",
            rainbow_speed: 5
        };

        function fetchState() {
            fetch('/api/state')
                .then(res => res.json())
                .then(data => {
                    state = data;
                    document.getElementById('brightness').value = state.brightness;
                    document.getElementById('brightnessValue').textContent = state.brightness;
                    document.getElementById('rainbowPattern').value = state.rainbow_pattern;
                    document.getElementById('rainbowSpeed').value = state.rainbow_speed;
                    document.getElementById('rainbowSpeedValue').textContent = state.rainbow_speed;
                    
                    const rgbToHex = (r, g, b) => '#' + [r, g, b].map(x => {
                        const hex = x.toString(16);
                        return hex.length === 1 ? '0' + hex : hex;
                    }).join('');
                    document.getElementById('colorPicker').value = rgbToHex(state.color[0], state.color[1], state.color[2]);
                    
                    updateUI();
                });
        }

        function updateUI() {
            document.querySelectorAll('.mode-btn').forEach(btn => btn.classList.remove('active'));
            document.getElementById('btn_' + state.mode).classList.add('active');

            // Make the actual current on/off state obvious: highlight
            // whichever button matches it, rather than the two buttons
            // just always looking different from each other regardless
            // of the real state.
            document.getElementById('btn_power_on').classList.toggle('active-on', state.is_on);
            document.getElementById('btn_power_off').classList.toggle('active-off', !state.is_on);

            const ul = document.getElementById('ticker-list');
            ul.innerHTML = '';
            state.tickers.forEach((t, i) => {
                let li = document.createElement('li');
                li.innerHTML = `<span>${t}</span> <button onclick="removeTicker(${i})" style="padding: 2px 5px; background: #dc3545;">X</button>`;
                ul.appendChild(li);
            });

            const rgbToHex = (r, g, b) => '#' + [r, g, b].map(x => {
                const hex = x.toString(16);
                return hex.length === 1 ? '0' + hex : hex;
            }).join('');

            const rl = document.getElementById('rainbow-color-list');
            rl.innerHTML = '';
            state.rainbow_colors.forEach((c, i) => {
                let li = document.createElement('li');
                li.innerHTML = `<span style="display:inline-block; width:20px; height:20px; background:${rgbToHex(c[0],c[1],c[2])}; border-radius:3px; vertical-align:middle; margin-right:8px;"></span>` +
                    `<button onclick="removeRainbowColor(${i})" style="padding: 2px 5px; background: #dc3545;">X</button>`;
                rl.appendChild(li);
            });
        }

        function pushState() {
            fetch('/api/state', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(state)
            });
            updateUI();
        }

        function togglePower(isOn) {
            state.is_on = isOn;
            pushState();
        }

        function setMode(mode) {
            state.mode = mode;
            pushState();
        }

        function stepBrightness(delta) {
            const slider = document.getElementById('brightness');
            const newVal = Math.max(0, Math.min(255, parseInt(slider.value) + delta));
            slider.value = newVal;
            document.getElementById('brightnessValue').textContent = newVal;
            updateState();
        }

        function updateState() {
            state.brightness = parseInt(document.getElementById('brightness').value);
            const hex = document.getElementById('colorPicker').value;
            state.color = [
                parseInt(hex.slice(1, 3), 16),
                parseInt(hex.slice(3, 5), 16),
                parseInt(hex.slice(5, 7), 16)
            ];
            pushState();
        }

        function addTicker() {
            const input = document.getElementById('newTicker');
            if (input.value && !state.tickers.includes(input.value.toUpperCase())) {
                state.tickers.push(input.value.toUpperCase());
                input.value = '';
                pushState();
            }
        }

        function removeTicker(index) {
            state.tickers.splice(index, 1);
            pushState();
        }

        function addRainbowColor() {
            const hex = document.getElementById('newRainbowColor').value;
            state.rainbow_colors.push([
                parseInt(hex.slice(1, 3), 16),
                parseInt(hex.slice(3, 5), 16),
                parseInt(hex.slice(5, 7), 16)
            ]);
            pushState();
        }

        function removeRainbowColor(index) {
            if (state.rainbow_colors.length <= 1) return; // always keep at least one color
            state.rainbow_colors.splice(index, 1);
            pushState();
        }

        function updateRainbowSettings() {
            state.rainbow_pattern = document.getElementById('rainbowPattern').value;
            state.rainbow_speed = parseInt(document.getElementById('rainbowSpeed').value);
            pushState();
        }

        fetchState();
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/state', methods=['GET', 'POST'])
def handle_state():
    global state
    if request.method == 'POST':
        data = request.json or {}

        if 'rainbow_speed' in data:
            try:
                data['rainbow_speed'] = max(1, min(int(data['rainbow_speed']), 10))
            except (TypeError, ValueError):
                data.pop('rainbow_speed', None)

        if 'rainbow_pattern' in data and data['rainbow_pattern'] not in ('wave', 'cycle'):
            data.pop('rainbow_pattern', None)

        if 'rainbow_colors' in data:
            try:
                cleaned = []
                for c in data['rainbow_colors']:
                    r, g, b = c
                    cleaned.append([max(0, min(int(r), 255)), max(0, min(int(g), 255)), max(0, min(int(b), 255))])
                data['rainbow_colors'] = cleaned if cleaned else state['rainbow_colors']
            except (TypeError, ValueError):
                data.pop('rainbow_colors', None)

        state.update(data)
        return jsonify({"status": "success"})
    return jsonify(state)

# --- 5. GRAPHICS DRAWING & LED MAPPING ---
def display_image_on_matrix(strip, image):
    """ Maps a 40x32 PIL image onto the user's specific LED matrix routing """
    image = image.convert('RGB')
    for y in range(ledHeight):
        for x in range(ledWidth):
            r, g, b = image.getpixel((x, y))
            led_index = int(ledMappingMatrix[y][x])
            strip.setPixelColor(led_index, Color(r, g, b))
    strip.show()

def draw_custom_text(image, text, x_start, y_start, color_rgb):
    """ Draws text pixel-by-pixel onto a PIL image using the CUSTOM_FONT dictionary. """
    x_current = x_start
    for char in text:
        char_upper = char.upper()
        if char_upper in CUSTOM_FONT:
            char_matrix = CUSTOM_FONT[char_upper]
            height, width = char_matrix.shape
            
            # Map the 10-pixel height layout to the board
            for r in range(height):
                for c in range(width):
                    if char_matrix[r][c] == 1:
                        if 0 <= x_current + c < ledWidth and 0 <= y_start + r < ledHeight:
                            image.putpixel((x_current + c, y_start + r), color_rgb)
            
            # Advance X position by the width of the letter + 1 pixel for kerning/spacing
            x_current += width + 1 
        else:
            # If a character isn't found in our dictionary, leave space for it
            x_current += 5


def get_weather_category(weathercode):
    """ Collapses Open-Meteo's WMO weather codes into the four icon
    categories we can actually draw recognizably on a low-res matrix. """
    if weathercode in (0, 1):
        return "sunny"
    elif weathercode in (71, 73, 75, 77, 85, 86):
        return "snow"
    elif weathercode in (51, 53, 55, 56, 57, 61, 63, 65, 66, 67, 80, 81, 82, 95, 96, 99):
        return "rain"
    else:  # 2, 3, 45, 48, and any unrecognized code
        return "cloudy"


WEATHER_ICON_COLORS = {
    "sunny": (255, 180, 0),
    "cloudy": (180, 180, 180),
    "rain": (40, 130, 255),
    "snow": (210, 235, 255),
}


def get_weather():
    """ Fetch current temperature, today's high/low, and a weather category
    from Open-Meteo for Richmond, BC. Returns
    (current_temp, low_temp, high_temp, category) on success, or None if
    every attempt fails (caller falls back to a "NO DATA" display).
    """
    url = (
        "https://api.open-meteo.com/v1/forecast"
        "?latitude=49.16&longitude=-123.13"
        "&current_weather=true"
        "&daily=temperature_2m_max,temperature_2m_min"
        "&timezone=America%2FVancouver"
        "&forecast_days=1"
    )
    headers = {"User-Agent": "Mozilla/5.0 (LED-Matrix-Display/1.0)"}

    for attempt in range(3):
        try:
            res = requests.get(url, headers=headers, timeout=8).json()

            if "current_weather" not in res:
                # Open-Meteo returns a normal 200 with an {"error": true,
                # "reason": "..."} body for bad requests/rate limiting,
                # rather than an HTTP error code - so a KeyError here is
                # usually the API telling us something, not a code bug.
                # Print the raw body so a repeat failure is diagnosable.
                raise KeyError(f"'current_weather' missing from response: {res}")

            current_temp = round(res["current_weather"]["temperature"])
            weathercode = res["current_weather"]["weathercode"]
            low_temp = round(res["daily"]["temperature_2m_min"][0])
            high_temp = round(res["daily"]["temperature_2m_max"][0])

            return (current_temp, low_temp, high_temp, get_weather_category(weathercode))
        except Exception as e:
            print(f"[get_weather] attempt {attempt + 1}/3 failed: {e}")
            traceback.print_exc()
            time.sleep(1)

    return None


def draw_weather_icon(draw, x, y, category):
    """ Draws a small (~11x11 px) weather icon with its top-left corner at
    (x, y). The matrix is far too low-res for real icon glyphs, so these
    are minimal, high-contrast silhouettes, each in a single color that
    identifies the condition (see WEATHER_ICON_COLORS). """
    color = WEATHER_ICON_COLORS.get(category, (200, 200, 200))

    if category == "sunny":
        # A solid circular sun with 8 rays (cardinal + diagonal) clearly
        # radiating outward, rather than a small blob that could be
        # mistaken for anything else.
        cx, cy, r = x + 5, y + 5, 3
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)
        draw.line([cx, y, cx, y + 1], fill=color)              # N
        draw.line([cx, y + 9, cx, y + 10], fill=color)          # S
        draw.line([x, cy, x + 1, cy], fill=color)                # W
        draw.line([x + 9, cy, x + 10, cy], fill=color)          # E
        draw.line([x + 1, y + 1, x + 2, y + 2], fill=color)      # NW
        draw.line([x + 9, y + 1, x + 8, y + 2], fill=color)      # NE
        draw.line([x + 1, y + 9, x + 2, y + 8], fill=color)      # SW
        draw.line([x + 9, y + 9, x + 8, y + 8], fill=color)      # SE

    elif category == "cloudy":
        draw.ellipse([x, y + 3, x + 6, y + 9], fill=color)
        draw.ellipse([x + 4, y + 1, x + 11, y + 9], fill=color)
        draw.rectangle([x + 2, y + 7, x + 10, y + 9], fill=color)

    elif category == "rain":
        # A single raindrop/teardrop shape - pointed top, rounded bottom -
        # with no cloud above it.
        cx = x + 5
        draw.polygon([(cx, y), (x + 1, y + 6), (x + 9, y + 6)], fill=color)
        draw.ellipse([x, y + 3, x + 10, y + 10], fill=color)

    else:  # snow - a 4-line (8-point) snowflake, no cloud
        cx, cy = x + 5, y + 5
        draw.line([cx, y, cx, y + 10], fill=color)                  # vertical
        draw.line([x, cy, x + 10, cy], fill=color)                  # horizontal
        draw.line([x + 1, y + 1, x + 9, y + 9], fill=color)         # diagonal \
        draw.line([x + 1, y + 9, x + 9, y + 1], fill=color)         # diagonal /
        # short branch ticks near each arm's tip for a more snowflake-like look
        draw.point([(cx - 1, y + 2), (cx + 1, y + 2), (cx - 1, y + 8), (cx + 1, y + 8)], fill=color)
        draw.point([(x + 2, cy - 1), (x + 2, cy + 1), (x + 8, cy - 1), (x + 8, cy + 1)], fill=color)


# yfinance talks to Yahoo's unofficial endpoints, which are increasingly
# strict about traffic that doesn't look like a real browser. Reusing one
# session with a normal User-Agent significantly cuts down on 429 "Too Many
# Requests" / empty-dataframe responses compared to yfinance's bare default.
_yf_session = requests.Session()
_yf_session.headers.update({"User-Agent": "Mozilla/5.0 (LED-Matrix-Display/1.0)"})


def get_stock_data(ticker):
    """ Fetch intraday data for graphing, with fallbacks for when the
    market is closed (weekends/holidays) or Yahoo briefly rate-limits us.
    Returns (current_price, price_history) or (None, None) if every
    attempt fails.
    """
    attempts = [
        ("1d", "5m"),
        ("5d", "15m"),   # falls back across the weekend / after-hours
    ]

    for period, interval in attempts:
        for attempt in range(2):
            try:
                tick = yf.Ticker(ticker, session=_yf_session)
                hist = tick.history(period=period, interval=interval)
                if hist.empty:
                    raise ValueError(f"empty history for period={period} interval={interval}")

                current_price = round(hist['Close'].iloc[-1], 2)
                prices = hist['Close'].tolist()
                return current_price, prices
            except Exception as e:
                print(f"[get_stock_data:{ticker}] {period}/{interval} attempt {attempt + 1}/2 failed: {e}")
                traceback.print_exc()
                time.sleep(1)

    # Last resort: try to at least get a live price even with no history,
    # so the ticker isn't showing "NODATA" purely because history failed.
    try:
        tick = yf.Ticker(ticker, session=_yf_session)
        price = tick.fast_info.get("lastPrice")
        if price:
            return round(price, 2), None
    except Exception as e:
        print(f"[get_stock_data:{ticker}] fast_info fallback failed: {e}")
        traceback.print_exc()

    return None, None

def interpolate_rainbow(colors, t):
    """ Given a list of [r,g,b] colors and a position t in [0,1) that wraps
    around the whole list, returns a smoothly blended (r,g,b) between
    whichever two colors t falls between. This is what lets the rainbow
    mode "scroll" or "cycle" smoothly rather than hard-cutting between
    colors. """
    n = len(colors)
    if n == 0:
        return (0, 0, 0)
    if n == 1:
        return tuple(colors[0])

    t = t % 1.0
    scaled = t * n
    i = int(scaled) % n
    frac = scaled - int(scaled)
    c1, c2 = colors[i], colors[(i + 1) % n]
    return tuple(int(c1[k] + (c2[k] - c1[k]) * frac) for k in range(3))


# --- 6. MAIN LED THREAD LOOP ---
def led_controller():
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    strip.begin()

    current_ticker_idx = 0
    loop_counter = 0
    cached_weather = None
    rainbow_offset = 0.0

    while True:
        try:
            strip.setBrightness(state["brightness"])

            if not state["is_on"]:
                for i in range(strip.numPixels()):
                    strip.setPixelColor(i, Color(0, 0, 0))
                strip.show()
                time.sleep(0.5)
                continue

            # --- MODE 1: LIGHT PANEL ---
            if state["mode"] == "light_panel":
                r, g, b = state["color"]
                color = Color(r, g, b)
                for i in range(strip.numPixels()):
                    strip.setPixelColor(i, color)
                strip.show()
                time.sleep(0.5)

            # --- MODE 2: TIME & WEATHER ---
            elif state["mode"] == "time_weather":
                img = Image.new('RGB', (ledWidth, ledHeight), color=(0, 0, 0))
                draw = ImageDraw.Draw(img)

                if loop_counter % 60 == 0:
                    cached_weather = get_weather()
                    print(f"Weather data captured: {cached_weather}")

                tz = pytz.timezone('America/Vancouver')
                now = datetime.now(tz)
                time_val = now.strftime("%I:%M").lstrip('0')
                am_pm = now.strftime("%p")

                # Line 1 (y=0): time and AM/PM together
                draw_custom_text(img, f"{time_val} {am_pm}", 1, 0, (255, 255, 255))

                if cached_weather is not None:
                    current_temp, low_temp, high_temp, category = cached_weather

                    # Line 2 (y=11): current temperature + a color-coded icon
                    # for the current condition (sunny/rain/cloudy/snow)
                    temp_str = f"{current_temp}C"
                    draw_custom_text(img, temp_str, 1, 11, (255, 255, 255))
                    icon_x = 1 + len(temp_str) * 5 + 3
                    draw_weather_icon(draw, icon_x, 11, category)

                    # Line 3 (y=22): today's temperature range
                    range_str = f"{low_temp}-{high_temp}C"
                    draw_custom_text(img, range_str, 1, 22, (0, 200, 255))
                else:
                    draw_custom_text(img, "NO DATA", 1, 11, (255, 0, 0))

                display_image_on_matrix(strip, img)
                time.sleep(1)
                loop_counter += 1

            # --- MODE 3: STOCK TRADING ---
            elif state["mode"] == "stock_trading":
                if not state["tickers"]:
                    time.sleep(1)
                    continue

                ticker = state["tickers"][current_ticker_idx]
                price, history = get_stock_data(ticker)

                img = Image.new('RGB', (ledWidth, ledHeight), color=(0, 0, 0))
                draw = ImageDraw.Draw(img) # Draw is still used exclusively for the graph line

                if price is not None:
                    if price >= 1000:
                        price_str = f"{price:.0f}"
                    else:
                        price_str = f"{price:.2f}"
                    price_str = price_str[:6]

                    # Using custom font mapping for text
                    draw_custom_text(img, ticker[:6], 1, 0, (255, 255, 0))
                    draw_custom_text(img, price_str, 1, 11, (255, 255, 255))

                    # Shifted the mini line graph downward (rows 22 to 31) so it doesn't overlap text
                    if history and len(history) > 1:
                        min_p, max_p = min(history), max(history)
                        diff = max_p - min_p if max_p - min_p != 0 else 1
                    
                        points = []
                        step = max(1, len(history) // 40)
                        sampled = history[::step][:40] 
                    
                        for x, p in enumerate(sampled):
                            normalized_y = 31 - int(((p - min_p) / diff) * 9)
                            points.append((x, normalized_y))
                    
                        if len(points) > 1:
                            graph_color = (0, 255, 0) if history[-1] >= history[0] else (255, 0, 0)
                            draw.line(points, fill=graph_color, width=1)
                else:
                    draw_custom_text(img, "NODATA", 1, 11, (255, 0, 0))

                display_image_on_matrix(strip, img)
                time.sleep(5)
                current_ticker_idx = (current_ticker_idx + 1) % len(state["tickers"])

            # --- MODE 4: RAINBOW ---
            elif state["mode"] == "rainbow":
                colors = state.get("rainbow_colors") or [[255, 0, 0]]
                pattern = state.get("rainbow_pattern", "wave")
                speed = max(1, min(int(state.get("rainbow_speed", 5)), 10))

                img = Image.new('RGB', (ledWidth, ledHeight), color=(0, 0, 0))

                if pattern == "cycle":
                    # Whole panel is one color at a time, smoothly fading
                    # to the next color in the user's list.
                    color = interpolate_rainbow(colors, rainbow_offset)
                    for x in range(ledWidth):
                        for y in range(ledHeight):
                            img.putpixel((x, y), color)
                else:
                    # "wave": each column gets a color based on its position
                    # plus the current time offset, so the whole list of
                    # colors visibly scrolls left-to-right across the panel.
                    for x in range(ledWidth):
                        t = (x / ledWidth) + rainbow_offset
                        color = interpolate_rainbow(colors, t)
                        for y in range(ledHeight):
                            img.putpixel((x, y), color)

                display_image_on_matrix(strip, img)
                # `speed` (1-10) is the user-facing "frequency" control -
                # higher speed advances the offset further per frame, so
                # the scroll/fade moves faster.
                rainbow_offset = (rainbow_offset + speed / 400.0) % 1.0
                time.sleep(0.05)

        except Exception as e:
            # A bug in any single mode (bad data, a display glitch,
            # etc.) should never be able to permanently freeze the
            # whole board the way the missing `traceback` import did
            # previously - log it and keep the loop alive instead.
            print(f"[led_controller] frame error: {e}")
            traceback.print_exc()
            time.sleep(1)


if __name__ == '__main__':
    # NOTE: Flask's debug reloader re-executes this whole script in a second
    # ("monitor") process to watch for code changes. Since led_thread.start()
    # runs unconditionally at the top level, debug=True previously caused
    # TWO independent led_controller threads - one per process, each with
    # its own default `state` - to write to the same physical LED strip at
    # once. That's what caused the periodic flash back to Time & Weather:
    # the monitor process's thread never received your mode changes (they
    # only reached the real worker process's `state`), so it kept redrawing
    # its own stale time_weather frame over whatever the real process had
    # just set.
    #
    # Code that drives physical hardware should never run twice like this,
    # so both debug mode and the reloader are disabled outright rather than
    # just worked around.
    led_thread = threading.Thread(target=led_controller, daemon=True)
    led_thread.start()

    print("Starting WebUI. Access via http://<Raspberry-Pi-IP-Address>:8080")
    app.run(host='0.0.0.0', port=8080, debug=False, use_reloader=False)
