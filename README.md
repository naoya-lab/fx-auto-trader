# FX Auto Trader

iPhoneから開発し、まずは過去データで売買ルールを試すための学習用プロジェクトです。

## いま入っているもの

- CSV形式のOHLCデータ読み込み
- 短期・長期移動平均線のクロスを使う、買いのみの簡易バックテスト
- スプレッドとスリッページを差し引いた損益（pips・円）集計
- 取引数量の指定（初期値は例として1万通貨）
- サンプルデータと、実行用スクリプト

売買シグナルは確定した足の後、次の足の始値で約定する簡易ルールです。円損益はJPYが決済通貨のペア（例：USD/JPY）を前提に、損益pips × pip幅 × 取引数量で計算します。初期取引数量1万通貨は例なので変更できます。必要証拠金、資金曲線、スワップ、税金、約定拒否などは未対応です。サンプルデータは架空データです。

## Codespacesで動かす

初回だけ依存関係を入れます。

```bash
python -m pip install -e .
```

サンプルでバックテストを実行します。

```bash
python scripts/run_backtest.py data/sample_ohlc.csv
```

期間やコストを変える例：

```bash
python scripts/run_backtest.py data/sample_ohlc.csv --fast 3 --slow 5 --spread 1.0 --slippage 0.2 --units 10000
```

CSVは `timestamp,open,high,low,close` の列を用意してください。円損益の計算はJPYが決済通貨のペアで使用してください。USD/JPYのpip幅は0.01を想定しています。別通貨ペアでは円換算に別の為替レートが必要です。

## テスト

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
node --test tests/browser.test.cjs
```

ブラウザ側の回帰テストにはNode.js 18以上を使用します。

## 安全上の範囲

この段階ではFX会社への接続、認証情報、発注機能はありません。バックテスト結果は将来の利益を保証しません。実データで検証し、デモ取引、損失制限や障害時停止などを別途確認するまでは実口座に接続しないでください。
