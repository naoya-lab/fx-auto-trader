# FX Auto Trader

iPhoneから開発し、まずは過去データで売買ルールを試すための学習用プロジェクトです。

## いま入っているもの

- CSV形式のOHLCデータ読み込み
- 短期・長期移動平均線のクロスを使う、買いのみの簡易バックテスト
- スプレッドとスリッページを差し引いた損益（pips）集計
- サンプルデータと、実行用スクリプト

売買シグナルは確定した足の後、次の足の始値で約定する簡易ルールです。ポジションサイズ、資金曲線、スワップ、税金、約定拒否などはまだ扱いません。サンプルデータは動作確認用の架空データで、収益性を示すものではありません。

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
python scripts/run_backtest.py data/sample_ohlc.csv --fast 3 --slow 5 --spread 1.0 --slippage 0.2
```

CSVは `timestamp,open,high,low,close` の列を用意してください。USD/JPYの標準的なpip幅を想定して初期値を0.01にしています。別通貨ペアではコード側の `pip_size` を適切に変更してください。

## テスト

```bash
python -m unittest discover -s tests -v
```

## 安全上の範囲

この段階ではFX会社への接続、認証情報、発注機能はありません。バックテスト結果は将来の利益を保証しません。実データで検証し、デモ取引、損失制限や障害時停止などを別途確認するまでは実口座に接続しないでください。
