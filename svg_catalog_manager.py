"""
█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█
  
   ｓｖｇ－ｃａｔａｌｏｇ－ｍａｎａｇｅｒ ™        ベクター  アーカイブ  システム
   ［ Ｖ Ａ Ｐ Ｏ Ｒ   Ｌ Ｉ Ｂ Ｒ Ａ Ｒ Ｙ   Ｉ Ｎ Ｔ Ｅ Ｒ Ｆ Ａ Ｃ Ｅ ］
     
   視覚記号管理装置  //  ２０８６  ＥＤＩＴＩＯＮ  ／  ｓｙｍｂｏｌ  ｓｔｏｒａｇｅ
     
█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█

   Signal curation // Vector memory registry system
   Ａｕｔｈｏｒ  ：：  Duygu  Dağdelen  ［ ２０２５－１２－１９ ］
    
█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█
"""

import json
import requests
import base64
import re
from getpass import getpass

class SVGCatalogManager:

    def __init__(self):
        # Config for the remote data store
        self.provider_id = "dduyg"
        self.collection_id = "LiminalLoop"
        self.target_file = "catalog.svgs.json"
        self.base_api_url = f"https://api.github.com/repos/{self.provider_id}/{self.collection_id}/contents/{self.target_file}"
        self.session_headers = {}

    def parse_vector_data(self, raw_svg):
        """Extracts spatial dimensions and path definitions from raw SVG strings."""
        viewbox_search = re.search(r'viewBox=["\']([^"\']+)["\']', raw_svg)
        viewbox = viewbox_search.group(1) if viewbox_search else "0 0 100 100"
        
        content_search = re.search(r'<svg[^>]*>(.*)</svg>', raw_svg, re.DOTALL)
        inner_paths = content_search.group(1).strip() if content_search else raw_svg
        return viewbox, inner_paths

    def serialize_with_compact_arrays(self, dataset):
        pretty_json = json.dumps(dataset, indent=2)
        
        def inline_list(match):
            items = [item.strip() for item in match.group(1).split(',')]
            return f'"tags": [{", ".join(items)}]'

        return re.sub(r'"tags":\s*\[(.*?)\]', inline_list, pretty_json, flags=re.DOTALL)

    def execute_sync(self):
      print("\n")
      print("███████  Ｓ Ｖ Ｇ   Ｃ Ａ Ｔ Ａ Ｌ Ｏ Ｇ   Ｍ Ａ Ｎ Ａ Ｇ Ｅ Ｒ  ███████")
      print("        ◢◤  視覚シンボル同期インターフェース  ◥◣")
      print("        ▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂\n")
        
        access_credential = getpass("┌─[ＡＵＴＨ]\n└──> Access Token: ")
        self.session_headers = {
            "Authorization": f"token {access_credential}",
            "Accept": "application/vnd.github.v3+json"
        }

        # Fetch current data state
        try:
            response = requests.get(self.base_api_url, headers=self.session_headers)
            response.raise_for_status()
        except Exception as error:
            print(f"⊗ Error: {error}")
            return

        remote_metadata = response.json()
        raw_encoded_content = remote_metadata['content']
        current_dataset = json.loads(base64.b64decode(raw_encoded_content + "===").decode('utf-8'))
        last_commit_hash = remote_metadata['sha']
        
        existing_registry_ids = {entry['id'] for entry in current_dataset}
        staged_entries = []
        
        # Ingestion Loop
        print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("［待機］ Awaiting input <svg> payloads to stage")
        print("→ To finalize batch, press ENTER on empty input")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
        
        while True:
            print(f"\n--- Staging Item #{len(staged_entries) + 1} ---")
            raw_input_svg = input("Enter <svg> code: ").strip()
            
            if not raw_input_svg:
                break
                
            while True:
                asset_id = input("Assign ID: ").strip().lower().replace(" ", "-")
                if not asset_id:
                    print("Error: Asset ID is mandatory.")
                    continue
                
                if asset_id in existing_registry_ids or any(e['id'] == asset_id for e in staged_entries):
                    print(f"⚠️ ID '{asset_id}' already exists!")
                    resolution = input("Override existing entry? (over) or assign new ID? (new): ").lower()
                    if resolution == 'over': break
                else:
                    break
            
            metadata_tags = input("Tags (comma separated): ")
            tag_list = [t.strip().lower() for t in metadata_tags.split(",") if t.strip()]
            
            viewbox, svg_path = self.parse_vector_data(raw_input_svg)
            
            staged_entries.append({
                "id": asset_id,
                "viewBox": viewbox,
                "tags": tag_list,
                "svg": svg_path
            })

        if not staged_entries:
            print("No new data entered. Session terminated.")
            return

        staged_ids = {e['id'] for e in staged_entries}
        # Merge datasets, prioritizing staged entries for overlaps
        finalized_dataset = [item for item in current_dataset if item['id'] not in staged_ids] + staged_entries
        
        processed_json = self.serialize_with_compact_arrays(finalized_dataset)
        
        commit_payload = {
            "message": f"[LIBRARY.EXPANDED]  with +{len(staged_entries)} item(s)",
            "content": base64.b64encode(processed_json.encode('utf-8')).decode('utf-8'),
            "sha": last_commit_hash
        }

        print(f"\n📡 Pushing {len(staged_entries)} svg(s) to catalog...")
        sync_response = requests.put(self.base_api_url, headers=self.session_headers, json=commit_payload)

        if sync_response.status_code in [200, 201]:
            print(f"\n☑️ Successfully expanded catalog with {len(staged_entries)} item(s).")
            print(f"Resource Path: {sync_response.json()['content']['html_url']}")
        else:
            print(f"❌ Commit failed: {sync_response.text}")

if __name__ == "__main__":
    manager = SVGCatalogManager()
    manager.execute_sync()
