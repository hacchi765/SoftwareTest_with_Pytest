# このリポジトリについて

このリポジトリは、Pythonを使用したソフトウェアテスト自動化の練習用プロジェクトです。Pytest を用いてテストケースを作成し、Docker コンテナを利用してテスト環境を構築します。初心者でも簡単にセットアップからテスト実行までを体験できるように、詳細な手順とガイドを提供しています。

## リポジトリの構成

```
PytestPractice/
├── .gitignore
├── Dockerfile
├── README.md
├── docker-compose.yml
├── requirements.txt
├── src/
└── tests/
```

- **Dockerfile**: テスト実行環境となるDockerイメージをビルドするための設定ファイルです。
- **src/**: アプリケーションのソースコードが含まれています。
- **tests/**: テストコードが含まれています。

## リポジトリのセットアップからテスト実行までの手順

### 1. リポジトリをクローン

1. GitHub のリポジトリページを開き、`git clone` 用の URL をコピーします。
2. ターミナル (もしくはコマンドプロンプト) でクローン先のディレクトリへ移動し、以下のコマンドを実行してください:

``` cmd
git clone <リポジトリURL>
cd <リポジトリ名>
```

例:
``` cmd
git clone https://github.com/your-account/python-testing-tutorial.git
cd python-testing-tutorial
```

### 2. Docker イメージのビルド

1. リポジトリ内にある `Dockerfile` や `docker-compose.yml` を利用して、Docker コンテナをビルドします。
2. 以下のコマンドを実行してください:

``` cmd
docker-compose build
```

### 3. コンテナの起動とテスト実行

#### 3.1 コンテナを起動してテスト (自動実行)

``` cmd
docker-compose up
```
- コンテナのログやテスト結果がターミナルに表示されます。

#### 3.2 テストを再実行したい場合

```
docker-compose run --rm python-testing-tutorial pytest
```

- `pytest` コマンドでテストを手動実行できます。  
- GUI (Streamlit) を使用している場合は、`docker-compose up` でコンテナを起動し、ブラウザ上でテストボタンをクリックしてテストを実行してください。

### 4. GUI へのアクセス (Streamlit など)

- ブラウザで `http://localhost:8501` (設定によりポート番号が異なる場合あり) にアクセスします。
- 「テスト実行」ボタンをクリックすると結果が画面に表示されます。

### 5. よくあるエラーと対策

1. **ModuleNotFoundError**  
   - `No module named 'src'` のようなエラーが出た場合は、以下を確認してください:
     - `src/__init__.py` が存在するか
     - `ENV PYTHONPATH="/app"` など Dockerfile でパスを通しているか
     - Pytest コマンドのオプションに問題がないか

2. **Docker ビルドの失敗**  
   - ネットワーク接続不良やキャッシュの問題でライブラリがインストールできない場合があります。  
   - `docker-compose build --no-cache` で再ビルドすると解決することがあります。

3. **ポートが競合している**  
   - すでに別アプリがポートを使っている可能性があります。  
   - `docker-compose.yml` でポート番号を変更してみてください。

### 6. テストケースの編集・追加

1. `tests` ディレクトリ内のファイルを編集し、新たなテストを追加できます。
2. テストコードを編集・保存した後は、コンテナ内で再度テストを実行するか、GUIからテストを実行すると変更が反映されます。

### 7. 終了とクリーンアップ

- コンテナを停止するときは、実行中のターミナルで `Ctrl + C` を押すか、別のターミナルから以下を実行してください:

```
docker-compose down
```

- すべての関連コンテナ、ネットワークを停止・破棄します。

### 8. 補足情報

- **Pytest のヘルプ**: 
``` python
pytest --help
```
- **Docker の基本コマンド**: 
``` cmd
docker ps
docker stop <ID>
docker rm <ID>
```
- **Streamlit**: [公式ドキュメント](https://docs.streamlit.io/) に詳しい設定例があります。

以上の手順を参考にすれば、初心者でもリポジトリのセットアップからテスト実行まで一通り体験できます。疑問点などがあれば適宜調べながら進めてみてください。
