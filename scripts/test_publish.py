import json, os, pathlib, shutil, subprocess, tempfile, unittest
SCRIPT = pathlib.Path(__file__).with_name('publish.sh').resolve()
class PublishTests(unittest.TestCase):
    def run_publish(self, version, channel, exists=False, policy="beta"):
        with tempfile.TemporaryDirectory() as d:
            root = pathlib.Path(d)
            (root/'scripts').mkdir()
            script = root/'scripts/publish.sh'
            shutil.copyfile(SCRIPT, script)
            if policy is not None:
                (root/'release-policy.json').write_text(json.dumps({'maximumChannel': policy}))
            (root/'dist').mkdir(); (root/'dist/package.exe').touch()
            gh = root/'gh'
            gh.write_text('#!/usr/bin/env python3\nimport json,os,sys\nif sys.argv[1:3]==["release","view"]: sys.exit(0 if os.environ["EXISTS"]=="1" else 1)\nopen("called.json","w").write(json.dumps(sys.argv[1:]))\n')
            gh.chmod(0o755)
            env = dict(os.environ, PATH=d+os.pathsep+os.environ['PATH'], VERSION=version, CHANNEL=channel, EXISTS=str(int(exists)), GITHUB_REPOSITORY='test/releases')
            result = subprocess.run(['bash',str(script)],cwd=d,env=env,capture_output=True,text=True)
            called=json.loads((root/'called.json').read_text()) if (root/'called.json').exists() else None
            return result.returncode, called
    def test_prereleases_never_become_latest(self):
        for channel in ['dev','beta']:
            code,args=self.run_publish('0.1.0-'+channel+'.4',channel)
            self.assertEqual(code,0); self.assertIn('--prerelease',args); self.assertIn('--latest=false',args)
    def test_stable_is_blocked_before_publication(self):
        code,args=self.run_publish('1.0.0','stable')
        self.assertNotEqual(code,0); self.assertIsNone(args)
    def test_missing_or_invalid_policy_fails_closed(self):
        for policy in [None, 'main', '']:
            code,args=self.run_publish('0.1.0-beta.4','beta',policy=policy)
            self.assertNotEqual(code,0); self.assertIsNone(args)
    def test_future_stable_requires_explicit_policy_change(self):
        code,args=self.run_publish('1.0.0','stable',policy='stable')
        self.assertEqual(code,0); self.assertIn('--latest',args)
    def test_dispatch_and_resolver_enforce_ceiling(self):
        workflow = SCRIPT.parents[1]/'.github/workflows/release.yml'
        text = workflow.read_text()
        self.assertIn('options: [dev, beta]', text)
        self.assertIn('checkReleasePolicy(process.cwd(), identity(', text)
    def test_duplicate_does_not_mutate_release(self):
        code,args=self.run_publish('0.1.0-beta.4','beta',True)
        self.assertNotEqual(code,0); self.assertIsNone(args)
    def test_wrong_channel_does_not_publish(self):
        code,args=self.run_publish('0.1.0-beta.4','stable')
        self.assertNotEqual(code,0); self.assertIsNone(args)
if __name__=='__main__': unittest.main()
