# Linux動的解析システム

----
## 準備
* ホストOS : ホームディレクトリ以下にMDAディレクトリ移動、sshd起動
* マネージャOS : ホームディレクトリ以下にanalysisディレクトリ移動、sshd起動
* ゲストOS : sshd起動

----
## 実行
1. マルウェア検体をマネージャの任意の場所に置く
2. ホストOSで、  
    `./analysis.py [マネージャの検体パス] [実行時間]`
  
----
## 実行結果
ホストOSの`~/MDA/data/sandbox_result/[検体md5]/[通し番号]/` にpcap保存



----
## 強制終了
未実装  
  

----
## 編集
* 7-Jun-2014 re-design
