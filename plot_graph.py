import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import numpy as np

# 1. 데이터 설정 (거리, 고도, 지명)
# [누적 거리, 고도, 지명, 구간 거리]
data = [
    [0, 170, "Saint-Jean-Pied-de-Port", 0],
    [5.0, 450, "Honto", 5.0],
    [7.6, 800, "Orisson", 2.6],
    [16.2, 1337, "Collado de Bentartea", 8.6],
    [20.2, 1430, "Collado de Lepoeder", 4.0],
    [24.2, 950, "Roncesvalles", 4.0]
]

distances = [row[0] for row in data]
elevations = [row[1] for row in data]
labels = [row[2] for row in data]
segments = [row[3] for row in data]

# 2. 그래프 스타일 설정
plt.style.use('ggplot') # 세련된 기본 스타일
fig, ax = plt.subplots(figsize=(12, 7))

# 부드러운 곡선 효과를 위한 보간 (옵션)
x_smooth = np.linspace(min(distances), max(distances), 300)
y_smooth = np.interp(x_smooth, distances, elevations)

# 고도 그래프 그리기 (채우기 효과)
ax.fill_between(x_smooth, y_smooth, color="#E67E22", alpha=0.3)
ax.plot(x_smooth, y_smooth, color="#D35400", linewidth=2.5, label="Elevation")

# 3. 각 지점 표시 및 지명/구간 거리 추가
for i in range(len(data)):
    # 지점 점 찍기
    ax.scatter(distances[i], elevations[i], color="#C0392B", s=60, zorder=5)
    
    # 지명 텍스트 (세로로 배치하여 가독성 확보)
    ax.text(distances[i], elevations[i] + 40, labels[i], 
            rotation=45, ha='left', fontsize=10, fontweight='bold')
    
    # 구간 거리 표시 (지점 사이 중간에 표시)
    if i > 0:
        mid_x = (distances[i-1] + distances[i]) / 2
        ax.text(mid_x, 150, f"{segments[i]}km", 
                ha='center', fontsize=9, color="#7F8C8D", style='italic')

# 4. 축 및 레이블 설정
ax.set_title("Camino de Santiago: SJPDP to Roncesvalles", fontsize=16, pad=20)
ax.set_xlabel("Distance (km)", fontsize=12)
ax.set_ylabel("Elevation (m)", fontsize=12)
ax.set_ylim(100, 1600)
ax.set_xlim(-1, 26)

# ---------------------------------------------------------
# 5. 로고 이미지 삽입 (Cursor에서 파일 경로만 수정하세요)
# ---------------------------------------------------------
def add_logo(path, zoom=0.1):
    try:
        img = mpimg.imread(path)
        imagebox = OffsetImage(img, zoom=zoom)
        # 로고 위치 (오른쪽 하단 여백: x=23km, y=250m 지점쯤)
        ab = AnnotationBbox(imagebox, (23, 250), frameon=False)
        ax.add_artist(ab)
    except FileNotFoundError:
        print("로고 파일을 찾을 수 없습니다. 경로를 확인해주세요.")

# 'logo.png'를 실제 파일명으로 바꾸거나 경로를 입력하세요.
# add_logo('your_logo_file.png', zoom=0.15) 
# ---------------------------------------------------------

plt.tight_layout()
plt.savefig('road_graph.png', dpi=150, bbox_inches='tight')
print("그래프가 'road_graph.png' 파일로 저장되었습니다!")
plt.show()
