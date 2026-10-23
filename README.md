# FX Auto Trader

iPhoneから開発し、まずは過去データの検証から始めるFX自動売買プロジェクトです。

## 現在の段階

**初期土台のみです。** このリポジトリには、FX会社への接続・発注機能はありません。初期設定では `backtest`（検証）モードのみを許可し、実注文を送るコードは追加していません。

## 開発の進め方

1. GitHub CodespacesでPython環境を開く
2. 売買ルールと過去データの形式を決め、バックテストを作る
3. スプレッド、スワップ、スリッページを含めて検証する
4. 接続先を決めてデモ口座で動作を確認する
5. 実運用を検討する場合は、注文・損失制限・通信断時の停止を別途確認する

バックテストの結果は将来の利益を保証しません。最初は実口座に接続しないでください。

## Codespacesで始める

GitHubでこのリポジトリを開き、**Code → Codespaces → Create codespace on main** を選びます。環境の作成後、ターミナルで実行します。

```bash
python -m pip install -e ".[dev]"
pytest
```

## ファイル構成

- `src/fx_auto_trader/settings.py`: 実行モードの設定。初期状態では `backtest` のみ
- `tests/`: 設定の安全動作を確認するテスト
- `.devcontainer/devcontainer.json`: Codespaces用Python環境

## 認証情報の扱い

- APIキー、パスワード、口座番号などをコードやコミットに書かない
- 公開リポジトリに変更しない
- 将来API接続を加える場合は、サービス側の安全なSecret管理を使い、まずデモ口座だけで確認する
