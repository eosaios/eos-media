import json, os, pathlib, subprocess, tempfile, unittest
SCRIPT = pathlib.Path(__file__).with_name('publish.sh').resolve()
class PublishTests(unittest.TestCase):
    def run_publish(self, version, channel, exists=False):
        with tempfile.TemporaryDirectory() as d:
            root = pathlib.Path(d)
            (root/'dist').mkdir(); (root/'dist/package.exe').touch()
            gh = root/'gh'
            gh.write_text('#!/usr/bin/env python3\nimport json,os,sys\nif sys.argv[1:3]==["release","view"]: sys.exit(0 if os.environ["EXISTS"]=="1" else 1)\nopen("called.json","w").write(json.dumps(sys.argv[1:]))\n')
            gh.chmod(0o755)
            env = dict(os.environ, PATH=d+os.pathsep+os.environ['PATH'], VERSION=version, CHANNEL=channel, EXISTS=str(int(exists)), GITHUB_REPOSITORY='test/releases')
            result = subprocess.run(['bash',str(SCRIPT)],cwd=d,env=env,capture_output=True,text=True)
            called=json.loads((root/'called.json').read_text()) if (root/'called.json').exists() else None
            return result.returncode, called
    def test_prereleases_never_become_latest(self):
        for channel in ['dev','beta']:
            code,args=self.run_publish('0.1.0-'+channel+'.4',channel)
            self.assertEqual(code,0); self.assertIn('--prerelease',args); self.assertIn('--latest=false',args)
    def test_stable(self):
        code,args=self.run_publish('1.0.0','stable')
        self.assertEqual(code,0); self.assertIn('--latest',args); self.assertNotIn('--prerelease',args)
    def test_duplicate_does_not_mutate_release(self):
        code,args=self.run_publish('0.1.0-beta.4','beta',True)
        self.assertNotEqual(code,0); self.assertIsNone(args)
    def test_wrong_channel_does_not_publish(self):
        code,args=self.run_publish('0.1.0-beta.4','stable')
        self.assertNotEqual(code,0); self.assertIsNone(args)
if __name__=='__main__': unittest.main()
