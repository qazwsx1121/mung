import folium
import pandas as pd
import webbrowser

# 엑셀 파일 경로 설정
csv_file_paths = [
    'C:/Users/지민혁/OneDrive/바탕 화면/mung/관광지.csv',
    'C:/Users/지민혁/OneDrive/바탕 화면/mung/동물병원.csv',
    'C:/Users/지민혁/OneDrive/바탕 화면/mung/놀이터.csv',          # 파일 경로 수정해야됨
    'C:/Users/지민혁/OneDrive/바탕 화면/mung/식당.csv',
    'C:/Users/지민혁/OneDrive/바탕 화면/mung/숙박집.csv',
    'C:/Users/지민혁/OneDrive/바탕 화면/mung/카페.csv'
]

# 전역 변수를 사용하여 마커 정보를 저장
markers = {}

def create_popup_content(row):
    content = f"{row['업체명']}"
    return content

# 팝업 내에서 리뷰를 수집할 수 있는 양식 추가
def create_popup_content(row):
    content = f"<strong>{row['업체명']}</strong><br>"
    
    # 리뷰를 수집하기 위한 양식 추가
    content += """
    <form id="reviewForm">
        <label for="review">리뷰 작성:</label><br>
        <textarea id="review" name="review" rows="4" cols="30"></textarea><br>
        <input type="button" value="제출" onclick="submitReview('{category}', '{marker_id}')">
    </form>
    """

    return content

# 리뷰 제출을 처리하는 JavaScript 함수
review_script = """
<script>
    function submitReview(category, marker_id) {{
        var reviewText = document.getElementById('review').value;
        alert('리뷰가 제출되었습니다');

        // 리뷰 데이터를 저장하거나 필요한 추가 작업을 수행할 수 있습니다.
        // 간단하게 리뷰 텍스트를 포함한 알림을 표시하고 있습니다.
    }}
</script>
"""

# Folium 지도 생성
m = folium.Map(location=[37.5, 127.0], zoom_start=10)

# 각 카테고리에 대한 레이어 생성
categories = ['관광지', '동물병원', '놀이터', '식당', '숙박집', '카페']
layer_groups = {category: folium.FeatureGroup(name=category) for category in categories}

# 엑셀 파일의 각 행에 대해 마커 추가    
markers = {}
for idx, csv_file_path in enumerate(csv_file_paths):
    df = pd.read_csv(csv_file_path, encoding='euc-kr')
    category = categories[idx]

    for index, row in df.iterrows():
        content = create_popup_content(row)
        content += review_script.format(category=category, marker_id=row['업체명'])  # 리뷰 스크립트 추가
        iframe = folium.IFrame(html=content, width=300, height=200)
        popup = folium.Popup(iframe, max_width=3000)

        # 각 카테고리에 따라 아이콘 변경
        icon_color = 'green' if category == '관광지' else 'red' if category == '동물병원' else 'blue' if category == '놀이터' else 'orange' if category == '식당' else 'black' if category == '숙박집' else 'purple'
        marker_icon = folium.Icon(color=icon_color, icon='leaf' if category == '관광지' else 'fa-medkit' if category == '동물병원' else 'fa-play' if category == '놀이터' else 'fa-cutlery' if category == '식당' else 'fa-bed' if category == '숙박집' else 'fa-coffee', prefix='fa')

        marker = folium.Marker(location=[row['위도'], row['경도']], popup=popup, icon=marker_icon)
        marker.add_to(layer_groups[category])
        markers[row['업체명']] = marker  # 마커를 딕셔너리에 저장

# 각 레이어를 Folium 맵에 추가
for category, layer_group in layer_groups.items():
    layer_group.add_to(m)

# 레이어 컨트롤을 사용하여 각 레이어를 토글할 수 있는 컨트롤 추가
folium.LayerControl().add_to(m)

# HTML 파일로 저장
m.save('map_with_popups_and_markers.html')

# 브라우저를 직접 열어서 확인
webbrowser.open('map_with_popups_and_markers.html', new=2)