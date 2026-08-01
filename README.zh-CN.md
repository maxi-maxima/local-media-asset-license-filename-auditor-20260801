# Local Media Asset License Filename Auditor

AI 生成演示和内容工具会产生大量图片、音频、视频素材。这个 CLI 会审计本地媒体文件，找出文件名或 sidecar 元数据中没有体现许可与来源的素材。

## 为什么现在值得做

开源项目越来越常发布截图、短视频、生成图和社媒素材。版权与来源错误会阻塞发布、演示和社区传播。

## 安装与运行

```bash
python -m local_media_asset_license_filename_auditor_20260801.cli examples/assets --summary
python -m local_media_asset_license_filename_auditor_20260801.cli examples/assets --missing-only --summary
python -m unittest discover -s tests
```

## 示例

```json
{
  "assets": [
    {"path": "Demo Shot.PNG", "status": "missing_license_marker", "suggested_filename": "demo-shot--license-needed.png"}
  ],
  "summary": {"total_assets": 1, "missing_license_markers": 1, "ok": 0}
}
```

## 路线图

- 可选安全重命名模式
- SPDX 风格 sidecar 模板
- CI 发布包门禁
