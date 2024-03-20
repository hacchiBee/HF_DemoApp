import streamlit as st
import pandas as pd
import requests
from io import StringIO
#import subprocess

#def commit_and_push_changes(commit_message):
    # Gitコマンドを使用して変更をコミットし、リモートリポジトリにプッシュする関数
    #subprocess.run(["git", "add", "new_data.csv"])
    #subprocess.run(["git", "commit", "-m", commit_message])
    #subprocess.run(["git", "pull", "origin", "main"])  # リモートリポジトリを最新の状態に更新
    #subprocess.run(["git", "push", "origin", "main"])

def main():
    st.title("地下埋設物管理デモアプリ")

    # GitHubリポジトリからCSVファイルをダウンロードする
    csv_url = "https://raw.githubusercontent.com/hacchiBee/HF_DemoApp/main/hfdemo_data.csv"
    response = requests.get(csv_url)
    csv_data = response.content.decode('utf-8')

    # CSVデータをデータフレームに読み込む
    df = pd.read_csv(StringIO(csv_data), parse_dates=[4], date_parser=lambda x: pd.to_datetime(x, format='%Y%m%d'))

    # URLのパラメータを取得
    query_params = st.query_params
    link_params = query_params.get("id", "1")

    # link_paramsがDataFrameのid列に存在するかどうかを確認
    if str(link_params) in df['id'].astype(str).values:
        # データを参照する
        st.write("### データ参照")
        selected_data = df[df['id'].astype(str) == str(link_params)]
        st.write(selected_data)

        # MAP生成
        selected_data_map = {'lat': selected_data['latitude'].tolist(), 'lon': selected_data['longitude'].tolist()}
        st.map(selected_data_map)
    else:
        st.write("### データ未登録タグ　番号："+link_params)
        # テキストボックスの入力値を受け取る
        latitude = st.text_input("緯度", key="latitude")
        longitude = st.text_input("経度", key="longitude")
        name = st.text_input("名称")
        registration_date = st.text_input("登録日")
        jurisdiction = st.text_input("管轄")
        notes = st.text_input("# 備考")

        # データ登録ボタン
        if st.button("データ登録"):
            # バリデーション
            if latitude and longitude and name and registration_date and jurisdiction and notes:
                # 新しいデータをデータフレームに追加する
                new_row = pd.DataFrame({'id': [link_params], 'latitude': [latitude], 'longitude': [longitude], '名称': [name], '登録日': [registration_date], '管轄': [jurisdiction], '備考': [notes]})
                df = pd.concat([df, new_row], ignore_index=True)

                # データをCSVファイルに保存する
                csv_string = df.to_csv(index=False)
                with open('new_data.csv', 'w') as f:
                    f.write(csv_string)

                # データの変更をコミットしてリモートリポジトリにプッシュする
                commit_message = f"Added new data with ID: {link_params}"
                #commit_and_push_changes(commit_message)

                # メッセージを表示する
                st.success("新しいデータを登録し、変更をコミットしました。")
            else:
                st.warning("入力された情報が不完全です。全ての項目を入力してください。")

if __name__ == "__main__":
    main()
