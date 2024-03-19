import streamlit as st

# データの準備（仮のデータ）
#http://localhost:8502/?id=2
#http://10.170.21.71:8502/?id=2

data = {
    '1': {'name': '1', 'latitude': 35.68953, 'longitude': 139.69173},
    '2': {'name': '2', 'latitude': 40.71283, 'longitude': -74.00603},
    '3': {'name': '3', 'latitude': 51.50743, 'longitude': -0.12783},
}

# メインのStreamlitアプリケーションの定義
def main():
    st.title('User Information')

    # URLのパラメータを取得
    query_params = st.query_params
    id = query_params.get("id", "1")

    # パラメータに対応するユーザー情報を取得
    user = data.get(id)

    # ユーザー情報を表示
    if user:
        st.write(f"ID: {id}")
        st.write(f"Latitude: {user['latitude']}")
        st.write(f"Longitude: {user['longitude']}")
    else:
        st.write("User not found.")

    # MAP生成
    map_data = {'lat': [user['latitude']], 'lon': [user['longitude']]}
    st.markdown(
        f"""
        <style>
            /* CSS to change marker size */
            .leaflet-marker-icon {{
                width: 2px !important;
                height: 2px !important;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.map(map_data)

if __name__ == "__main__":
    main()
