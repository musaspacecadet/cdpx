import logging
import shutil
from pathlib import Path
from codegen import parser, generator, models

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(name)s:%(message)s')
logger = logging.getLogger(__name__)

def inspect_protocol(json_paths):
    protocol: parser.ProtocolDefinition = parser.parse_protocol_files(*json_paths)

    print("-" * 30)
    print(f"Successfully parsed protocol version: {protocol.version_major}.{protocol.version_minor}")
    print(f"Total domains found: {len(protocol.domains)}")
    print(f"Domains found: {', '.join(list(protocol.domains.keys()))}")
    print("-" * 30)

    # Inspect specific domain
    page_domain_name = 'Page'
    if page_domain_name in protocol.domains:
        page_domain = protocol.domains[page_domain_name]
        print(f"\nInspecting Domain: {page_domain.name}")
        print(f"  Description: {page_domain.description[:50]}...")
        print(f"  Types: {len(page_domain.types)}")
        print(f"  Commands: {len(page_domain.commands)}")
        print(f"  Events: {len(page_domain.events)}")

        nav_command_name = 'navigate'
        if nav_command_name in page_domain.commands:
            nav_command = page_domain.commands[nav_command_name]
            print(f"\n  Inspecting Command: {page_domain.name}.{nav_command.name}")
            print(f"    Parameters ({len(nav_command.parameters)}):")
            for param in nav_command.parameters:
                param_type = param.type_ref or f"array[{param.items.type_ref}]"
                optional_flag = " (optional)" if param.is_optional else ""
                print(f"      - {param.name}: {param_type}{optional_flag}")

        frame_type_id = 'Frame'
        if frame_type_id in page_domain.types:
            frame_type = page_domain.types[frame_type_id]
            print(f"\n  Inspecting Type: {page_domain.name}.{frame_type.id}")
            print(f"    Type: {frame_type.type.name}")
            if frame_type.type == parser.CdpType.OBJECT:
                print(f"    Properties ({len(frame_type.properties)}):")
                for prop in frame_type.properties[:5]:
                    prop_type = prop.type_ref or f"array[{prop.items.type_ref}]"
                    print(f"      - {prop.name}: {prop_type}")
    else:
        print(f"\nDomain '{page_domain_name}' not found in parsed protocol.")


def generate_ast(json_paths, output_path):
    if output_path.exists():
        logger.warning(f"Output path {output_path} already exists. Removing it.")
        try:
            if output_path.is_dir():
                shutil.rmtree(output_path)
            else:
                output_path.unlink()
        except OSError as e:
            logger.error(f"Failed to remove output path: {e}")
            return

    logger.info("Starting CDP AST generation...")
    logger.info(f"Protocol Definitions: {', '.join(str(p) for p in json_paths)}")
    logger.info(f"Output Directory: {output_path}")

    missing_files = [p for p in json_paths if not p.exists()]
    if missing_files:
        logger.error(f"Missing files: {', '.join(str(p) for p in missing_files)}")
        return

    protocol: models.ProtocolDefinition = parser.parse_protocol_files(*json_paths)
    logger.info(f"Parsed Protocol Version: {protocol.version_major}.{protocol.version_minor}")
    logger.info(f"Domains found: {len(protocol.domains)}")

    generator.generate_all(protocol, output_path)
    logger.info("Generation completed successfully.")


def main():
    
    script_dir = Path(__file__).parent.resolve()
    json_paths = [
        script_dir / 'browser_protocol.json',
        script_dir / 'js_protocol.json'
    ]
    output_path = script_dir / 'cdp'

    inspect_protocol(json_paths)
    generate_ast(json_paths, output_path)
    
if __name__ == "__main__":
    main()
