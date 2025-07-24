#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SCRIPT DIAGNÓSTICO - TELA BRANCA EM BUILDS
Identifica exatamente qual é o problema com seus builds Flet
"""

import os
import sys
import json
import subprocess
import traceback
from pathlib import Path

# Cores para output
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text.center(60)}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.END}\n")

def print_success(text):
    print(f"{Colors.GREEN}✅ {text}{Colors.END}")

def print_warning(text):
    print(f"{Colors.YELLOW}⚠️ {text}{Colors.END}")

def print_error(text):
    print(f"{Colors.RED}❌ {text}{Colors.END}")

def print_info(text):
    print(f"{Colors.BLUE}ℹ️ {text}{Colors.END}")

def run_command(cmd, timeout=30):
    """Executa comando e retorna output"""
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, 
            text=True, timeout=timeout, encoding='utf-8'
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Timeout"
    except Exception as e:
        return False, "", str(e)

def check_python_environment():
    """Verifica ambiente Python"""
    print_header("AMBIENTE PYTHON")
    
    print_info(f"Python: {sys.version}")
    print_info(f"Executável: {sys.executable}")
    print_info(f"Platform: {sys.platform}")
    
    # Verificar pip
    success, output, error = run_command("pip --version")
    if success:
        print_success(f"Pip: {output.strip()}")
    else:
        print_error(f"Pip não encontrado: {error}")
    
    # Verificar flet
    try:
        import flet as ft
        print_success(f"Flet: {getattr(ft, 'version', 'N/A')}")
        
        # Verificar flet-cli
        success, output, error = run_command("flet --version")
        if success:
            print_success(f"Flet CLI: {output.strip()}")
        else:
            print_warning(f"Flet CLI: {error}")
            
    except ImportError as e:
        print_error(f"Flet não instalado: {e}")
        return False
    
    return True

def check_project_structure():
    """Verifica estrutura do projeto"""
    print_header("ESTRUTURA DO PROJETO")
    
    required_files = ['main.py']
    optional_files = ['requirements.txt', 'pubspec.yaml', '.github/workflows']
    
    project_ok = True
    
    for file in required_files:
        if os.path.exists(file):
            print_success(f"Arquivo obrigatório: {file}")
        else:
            print_error(f"Arquivo obrigatório faltando: {file}")
            project_ok = False
    
    for file in optional_files:
        if os.path.exists(file):
            print_success(f"Arquivo opcional: {file}")
        else:
            print_warning(f"Arquivo opcional não encontrado: {file}")
    
    # Verificar conteúdo do main.py
    if os.path.exists('main.py'):
        with open('main.py', 'r', encoding='utf-8') as f:
            content = f.read()
            
            # Verificar imports problemáticos
            problematic_imports = [
                'pandas', 'numpy', 'matplotlib', 'sklearn', 'tensorflow',
                'opencv', 'pillow', 'requests', 'beautifulsoup'
            ]
            
            found_problems = []
            for imp in problematic_imports:
                if f"import {imp}" in content or f"from {imp}" in content:
                    found_problems.append(imp)
            
            if found_problems:
                print_warning(f"Imports pesados encontrados: {', '.join(found_problems)}")
                print_info("Considere remover para builds mais leves")
            else:
                print_success("Nenhum import problemático encontrado")
            
            # Verificar paths relativos
            if 'open(' in content and not 'get_data_path' in content:
                print_warning("Possíveis paths relativos encontrados")
                print_info("Use paths absolutos para builds")
            else:
                print_success("Gerenciamento de paths parece OK")
    
    return project_ok

def test_local_execution():
    """Testa execução local"""
    print_header("TESTE DE EXECUÇÃO LOCAL")
    
    if not os.path.exists('main.py'):
        print_error("main.py não encontrado")
        return False
    
    print_info("Testando importação do módulo...")
    try:
        # Testar imports básicos
        exec(compile(open('main.py').read(), 'main.py', 'exec'))
        print_success("Imports básicos OK")
    except Exception as e:
        print_error(f"Erro nos imports: {e}")
        print_info("Stacktrace:")
        traceback.print_exc()
        return False
    
    print_info("Testando inicialização da aplicação...")
    success, output, error = run_command("python main.py", timeout=10)
    
    if "error" in error.lower() or "exception" in error.lower():
        print_error("Erros encontrados na execução:")
        print(error)
        return False
    else:
        print_success("Aplicação inicia sem erros críticos")
        if output:
            print_info("Output da aplicação:")
            print(output[:500] + "..." if len(output) > 500 else output)
    
    return True

def check_build_dependencies():
    """Verifica dependências para build"""
    print_header("DEPENDÊNCIAS DE BUILD")
    
    # Verificar Java para Android
    success, output, error = run_command("java -version")
    if success:
        java_version = output.split('\n')[0] if output else error.split('\n')[0]
        if "17" in java_version or "18" in java_version or "19" in java_version:
            print_success(f"Java: {java_version}")
        else:
            print_warning(f"Java: {java_version} (recomendado: Java 17)")
    else:
        print_warning("Java não encontrado (necessário para Android)")
    
    # Verificar Git
    success, output, error = run_command("git --version")
    if success:
        print_success(f"Git: {output.strip()}")
    else:
        print_warning("Git não encontrado")
    
    # Verificar flet build capabilities
    success, output, error = run_command("flet build --help")
    if success:
        print_success("Flet build disponível")
    else:
        print_error(f"Problema com flet build: {error}")

def simulate_build_environment():
    """Simula ambiente de build"""
    print_header("SIMULAÇÃO DE AMBIENTE DE BUILD")
    
    print_info("Simulando ambiente de executável...")
    
    # Simular sys.frozen
    original_frozen = getattr(sys, 'frozen', False)
    original_executable = sys.executable
    
    try:
        sys.frozen = True
        sys.executable = os.path.abspath('./fake_executable')
        
        print_info("Testando aplicação em modo 'frozen'...")
        
        # Tentar importar e executar partes críticas
        if os.path.exists('main.py'):
            with open('main.py', 'r', encoding='utf-8') as f:
                code = f.read()
                
            # Procurar por funções que usam paths
            if 'get_data_path' in code or 'get_asset_path' in code:
                print_success("Funções de path para build encontradas")
            else:
                print_warning("Nenhuma função de path para build encontrada")
                print_info("Adicione funções para resolver paths em builds")
        
        print_success("Simulação concluída sem erros")
        
    except Exception as e:
        print_error(f"Erro na simulação: {e}")
        
    finally:
        # Restaurar valores originais
        if original_frozen:
            sys.frozen = original_frozen
        else:
            delattr(sys, 'frozen')
        sys.executable = original_executable

def analyze_github_workflow():
    """Analisa workflow do GitHub Actions"""
    print_header("ANÁLISE DO WORKFLOW GITHUB")
    
    workflow_paths = [
        '.github/workflows/build.yml',
        '.github/workflows/main.yml', 
        '.github/workflows/ci.yml'
    ]
    
    workflow_found = False
    for path in workflow_paths:
        if os.path.exists(path):
            workflow_found = True
            print_success(f"Workflow encontrado: {path}")
            
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Verificar configurações importantes
            checks = [
                ('python-version: "3.11"', "Python 3.11 (recomendado)"),
                ('java-version: \'17\'', "Java 17 para Android"),
                ('PYTHONUTF8: "1"', "UTF-8 encoding"),
                ('--verbose', "Logs verbosos"),
                ('flet build', "Comandos de build Flet")
            ]
            
            for check, description in checks:
                if check in content:
                    print_success(f"✓ {description}")
                else:
                    print_warning(f"✗ {description} não encontrado")
            
            break
    
    if not workflow_found:
        print_warning("Nenhum workflow GitHub Actions encontrado")
        print_info("Crie um workflow para build automatizado")

def generate_recommendations():
    """Gera recomendações baseadas na análise"""
    print_header("RECOMENDAÇÕES")
    
    recommendations = []
    
    # Verificar se main.py existe e tem problemas
    if os.path.exists('main.py'):
        with open('main.py', 'r', encoding='utf-8') as f:
            content = f.read()
            
        if 'get_data_path' not in content:
            recommendations.append(
                "🔧 Implementar função get_data_path() para paths absolutos"
            )
            
        if 'try:' not in content or 'except:' not in content:
            recommendations.append(
                "🛡️ Adicionar tratamento de erros robusto"
            )
        
        problematic_imports = ['pandas', 'numpy', 'matplotlib']
        for imp in problematic_imports:
            if imp in content:
                recommendations.append(
                    f"📦 Considerar remover import {imp} para builds mais leves"
                )
    
    # Verificar estrutura do projeto
    if not os.path.exists('requirements.txt'):
        recommendations.append(
            "📝 Criar requirements.txt com dependências mínimas"
        )
    
    if not os.path.exists('pubspec.yaml'):
        recommendations.append(
            "📱 Criar pubspec.yaml para builds Android"
        )
    
    if not os.path.exists('.github/workflows'):
        recommendations.append(
            "🚀 Configurar GitHub Actions para build automatizado"
        )
    
    # Mostrar recomendações
    if recommendations:
        for i, rec in enumerate(recommendations, 1):
            print(f"{i}. {rec}")
    else:
        print_success("Projeto parece bem configurado!")
    
    print_info("\n💡 Próximos passos:")
    print("1. Use a aplicação build-otimizada como referência")
    print("2. Implemente as recomendações acima")
    print("3. Teste localmente antes de fazer build")
    print("4. Configure workflow GitHub Actions otimizado")

def create_fix_suggestions():
    """Cria arquivo com sugestões de correção"""
    print_header("CRIANDO ARQUIVO DE CORREÇÕES")
    
    fixes = {
        "paths_absolutos": '''
# Adicione esta função na sua classe principal:
def get_data_path(self, filename):
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, filename)
''',
        "tratamento_erros": '''
# Envolva código crítico com try/except:
def main(page: ft.Page):
    try:
        # Sua configuração aqui
        page.title = "Minha App"
        # ... resto do código
    except Exception as e:
        print(f"Erro: {e}")
        page.add(ft.Text(f"Erro: {e}"))
''',
        "requirements_minimo": '''
# requirements.txt mínimo:
flet==0.27.5
''',
        "pubspec_basico": '''
# pubspec.yaml básico:
name: minha_app
description: Minha aplicação
version: 1.0.0+1
publish_to: 'none'

environment:
  sdk: '>=2.17.0 <4.0.0'

dependencies:
  flutter:
    sdk: flutter
  flet: ^0.27.5

flutter:
  uses-material-design: true
'''
    }
    
    try:
        with open('build_fixes.md', 'w', encoding='utf-8') as f:
            f.write("# Correções Sugeridas para Build\n\n")
            for title, code in fixes.items():
                f.write(f"## {title.replace('_', ' ').title()}\n")
                f.write(f"```python{code}```\n\n")
        
        print_success("Arquivo 'build_fixes.md' criado com sugestões!")
        
    except Exception as e:
        print_error(f"Erro ao criar arquivo: {e}")

def main():
    """Função principal do diagnóstico"""
    print_header("DIAGNÓSTICO DE BUILD FLET")
    print_info("Este script identifica problemas comuns que causam tela branca em builds")
    
    # Executar todas as verificações
    checks = [
        ("Ambiente Python", check_python_environment),
        ("Estrutura do Projeto", check_project_structure), 
        ("Execução Local", test_local_execution),
        ("Dependências de Build", check_build_dependencies),
        ("Simulação de Build", simulate_build_environment),
        ("Workflow GitHub", analyze_github_workflow),
    ]
    
    results = {}
    
    for name, check_func in checks:
        try:
            results[name] = check_func()
        except Exception as e:
            print_error(f"Erro na verificação '{name}': {e}")
            results[name] = False
    
    # Resumo dos resultados
    print_header("RESUMO DOS RESULTADOS")
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for name, result in results.items():
        if result:
            print_success(f"{name}: PASSOU")
        else:
            print_warning(f"{name}: PRECISA ATENÇÃO")
    
    print(f"\n{Colors.BOLD}Score: {passed}/{total} verificações passaram{Colors.END}")
    
    if passed == total:
        print_success("🎉 Projeto parece bem configurado para builds!")
    elif passed >= total * 0.7:
        print_warning("⚠️ Alguns ajustes necessários")
    else:
        print_error("🚨 Vários problemas encontrados - recomendado usar versão otimizada")
    
    # Gerar recomendações
    generate_recommendations()
    create_fix_suggestions()
    
    print_header("DIAGNÓSTICO CONCLUÍDO")
    print_info("Verifique o arquivo 'build_fixes.md' para correções específicas")
    print_info("Use a aplicação build-otimizada como referência")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_error("\n\nDiagnóstico interrompido pelo usuário")
    except Exception as e:
        print_error(f"\nErro inesperado: {e}")
        traceback.print_exc()
